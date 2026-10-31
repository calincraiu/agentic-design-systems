"""
ADS Bridge - Listener  (paste into a GhPython / Python Script component)

Watches <repo>/.exchange/job.json for jobs posted by the Python tools and passes
the current job on to the rest of the definition.

Inputs (all Item access)
  active    bool  "Agent control": True = agent jobs drive the model, False = sliders do
  system    str   which design system this definition is, e.g. "tower"
  interval  int   how often to check for new jobs, in ms (optional, default 500)
Outputs
  job       str   the current job as JSON text, or None when the sliders are in control
  status    str   what the Listener is doing, for a Panel

How it works: a background timer reads job.json every `interval` ms. It answers
pings itself, rejects jobs it can't run, and for a real job it re-runs this
component, which outputs the job so the definition recomputes from it.

Runs in Rhino 7 (IronPython 2.7) and Rhino 8 (Python 3): no f-strings, and file
access goes through .NET's System.IO. Save the .gh file inside the course repo:
the Listener finds the repo by looking for pyproject.toml above the .gh file.
"""
import json
import os
import time

import System
import Rhino
import scriptcontext as sc

STALE_AFTER_S = 120  # ignore jobs older than this, e.g. left over from yesterday


def find_exchange(component):
    doc = component.OnPingDocument()
    path = doc.FilePath if doc is not None else None
    if not path:
        return None
    folder = os.path.dirname(path)
    while True:
        if os.path.exists(os.path.join(folder, "pyproject.toml")):
            return os.path.join(folder, ".exchange")
        parent = os.path.dirname(folder)
        if parent == folder:
            return None
        folder = parent


def read_json(path):
    try:
        if not System.IO.File.Exists(path):
            return None
        return json.loads(System.IO.File.ReadAllText(path))
    except Exception:
        return None  # locked or half-written: try again on the next tick


def write_json(path, data):
    tmp = path + ".tmp"
    System.IO.File.WriteAllText(tmp, json.dumps(data))
    for _ in range(20):
        try:
            System.IO.File.Copy(tmp, path, True)
            break
        except Exception:
            time.sleep(0.05)  # Python is reading it right now
    System.IO.File.Delete(tmp)


def is_fresh(job):
    return job is not None and time.time() - float(job.get("created", 0)) < STALE_AFTER_S


def answer(exchange, job, status, message, extra=None):
    result = {"job_id": job.get("job_id"), "status": status, "message": message}
    result.update(extra or {})
    write_json(os.path.join(exchange, "result.json"), result)


def stop_timer(state):
    timer = state.pop("timer", None)
    if timer is not None:
        timer.Dispose()


def make_tick(component, exchange, state, active, system):
    def expire():
        component.ExpireSolution(True)

    def tick(_):
        # Runs on a background thread: an uncaught error here would crash Rhino.
        try:
            if component.OnPingDocument() is None:  # component deleted or document closed
                stop_timer(state)
                return
            job = read_job(exchange)
            if job is None or job.get("job_id") == state.get("seen") or not is_fresh(job):
                return
            state["seen"] = job.get("job_id")
            if job.get("kind") == "ping":
                answer(exchange, job, "pong", "Grasshopper is listening.",
                       {"system": system, "active": active, "rhino": str(Rhino.RhinoApp.Version)})
            elif job.get("system") != system:
                answer(exchange, job, "error", "The open Grasshopper definition is '%s', but this job is for '%s'. "
                       "Open the right definition." % (system, job.get("system")))
            elif not active:
                answer(exchange, job, "error", "Agent control is OFF in Grasshopper: set the 'Agent control' toggle to True.")
            else:
                Rhino.RhinoApp.InvokeOnUiThread(System.Action(expire))
        except Exception:
            pass
    return tick


def read_job(exchange):
    return read_json(os.path.join(exchange, "job.json"))


def start_timer(state, tick, interval):
    stop_timer(state)
    state["timer"] = System.Threading.Timer(System.Threading.TimerCallback(tick), None, interval, interval)


def run(component, active, system, interval):
    state = sc.sticky.setdefault("ads_listener_" + str(component.InstanceGuid), {})
    system = (system or "").strip()
    if not system:
        stop_timer(state)
        return None, "Set the 'system' input, e.g. a Panel containing: tower"
    exchange = find_exchange(component)
    if exchange is None:
        stop_timer(state)
        return None, "Save this definition inside the course repo folder first (the Listener looks for pyproject.toml)."
    if not System.IO.Directory.Exists(exchange):
        System.IO.Directory.CreateDirectory(exchange)

    current = read_job(exchange)
    if current is not None:
        state["seen"] = current.get("job_id")
    start_timer(state, make_tick(component, exchange, state, bool(active), system), int(interval or 500))

    if not active:
        return None, "Agent control OFF: the sliders drive the model."
    if is_fresh(current) and current.get("kind") == "generate" and current.get("system") == system:
        return json.dumps(current), "Running agent job %s" % current.get("job_id")
    return None, "Listening for '%s' jobs in %s" % (system, exchange)


job, status = run(ghenv.Component, active, system, interval)  # noqa: F821 (ghenv and inputs come from Grasshopper)
