"""
ADS Bridge - Writer  (paste into a GhPython / Python Script component)

Sends the definition's result back to the Python tools: writes geometry.json into
the job's run folder, then reports ok/error in <repo>/.exchange/result.json.
It answers each job once; when the sliders are in control it does nothing.

Inputs
  job     str     from the Listener (Item access)
  curves  Curve   the geometry to send back (List access, type hint: Curve)
  keys    str     names of extra values to send, e.g. "floor_height" (List access, optional)
  values  float   the extra values, in the same order as keys (List access, optional)
Outputs
  status  str     what was sent, for a Panel

Runs in Rhino 7 (IronPython 2.7) and Rhino 8 (Python 3).
"""
import json
import os
import time

import System
import Rhino
import scriptcontext as sc

STALE_AFTER_S = 120


def read_json(path):
    try:
        if not System.IO.File.Exists(path):
            return None
        return json.loads(System.IO.File.ReadAllText(path))
    except Exception:
        return None


def write_json(path, data):
    tmp = path + ".tmp"
    System.IO.File.WriteAllText(tmp, json.dumps(data))
    for _ in range(20):
        try:
            System.IO.File.Copy(tmp, path, True)
            break
        except Exception:
            time.sleep(0.05)
    System.IO.File.Delete(tmp)


def curve_points(curve):
    """Corner points of a polyline, or 64 points along any other curve."""
    points = None
    try:
        ok, polyline = curve.TryGetPolyline()
        if ok:
            points = list(polyline)
    except Exception:
        points = None
    if points is None:
        points = [curve.PointAt(t) for t in curve.DivideByCount(64, True)]
    coords = [[round(p.X, 4), round(p.Y, 4), round(p.Z, 4)] for p in points]
    if len(coords) > 1 and coords[0] == coords[-1]:
        coords.pop()  # closed polylines repeat their first point
    return coords


def as_value(v):
    try:
        return float(v)
    except Exception:
        return str(v)


def run(job, curves, keys, values):
    if not job:
        return "Waiting: no agent job (the sliders are in control)."
    job = json.loads(job)
    job_id = job["job_id"]
    result_path = os.path.join(job["exchange_dir"], "result.json")
    answered = sc.sticky.setdefault("ads_writer_answered", set())
    previous = read_json(result_path)
    if job_id in answered or (previous is not None and previous.get("job_id") == job_id):
        return "Already sent job %s." % job_id
    if time.time() - float(job.get("created", 0)) > STALE_AFTER_S:
        return "Ignoring stale job %s." % job_id

    answered.add(job_id)
    try:
        data = {
            "system": job.get("system"),
            "source": "grasshopper",
            "rhino": str(Rhino.RhinoApp.Version),
            "curves": [curve_points(c) for c in (curves or []) if c is not None],
        }
        for k, v in zip(keys or [], values or []):
            data[str(k)] = as_value(v)
        if not data["curves"]:
            raise ValueError("no curves arrived at the Writer: check the definition for red or orange components")
        write_json(os.path.join(job["run_dir"], "geometry.json"), data)
        write_json(result_path, {"job_id": job_id, "status": "ok", "message": "%d curves sent." % len(data["curves"])})
        return "Sent job %s: %d curves." % (job_id, len(data["curves"]))
    except Exception as e:
        write_json(result_path, {"job_id": job_id, "status": "error", "message": "Grasshopper Writer failed: %s" % e})
        return "Error in job %s: %s" % (job_id, e)


status = run(job, curves, keys, values)  # noqa: F821 (inputs come from Grasshopper)
