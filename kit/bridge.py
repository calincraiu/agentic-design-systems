"""The bridge between Python tools and Grasshopper: two files in a shared folder.

    Python  --writes-->  .exchange/job.json     --read by-->  GH Listener
    Python  <--reads--   .exchange/result.json  <--writes--   GH Writer (or Listener)

A job asks Grasshopper either to "ping" (are you there?) or to "generate" a design
from parameters. For a generate job, the Writer saves geometry.json into the job's
run folder and then reports ok/error in result.json. The Grasshopper side of this
protocol lives in kit/gh/.
"""
import json
import os
import time
import uuid

from .paths import exchange_dir

HINT = (
    "Check that Rhino is open, the definition (e.g. examples/tower/tower.gh) is open in "
    "Grasshopper, and its 'Agent control' toggle is True. `uv run kit ping` tests the connection."
)


class BridgeError(RuntimeError):
    pass


def _write_json(path, data):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    for _ in range(40):
        try:
            os.replace(tmp, path)  # atomic: Grasshopper never sees half a file
            return
        except PermissionError:  # Windows: Grasshopper is reading it right now
            time.sleep(0.05)
    raise BridgeError(f"Could not write {path}: the file stays locked.")


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError):
        return None  # missing, locked or half-written: try again shortly


def send(kind, system=None, params=None, run_dir=None):
    """Post a job for Grasshopper and return its id."""
    folder = exchange_dir()
    folder.mkdir(parents=True, exist_ok=True)
    job_id = time.strftime("%H%M%S-") + uuid.uuid4().hex[:6]
    _write_json(folder / "job.json", {
        "job_id": job_id,
        "kind": kind,
        "system": system,
        "params": params or {},
        "run_dir": str(run_dir.resolve()) if run_dir else None,
        "exchange_dir": str(folder.resolve()),
        "created": time.time(),
    })
    return job_id


def wait(job_id, timeout):
    """Wait for Grasshopper's answer to a job; None if it never comes."""
    path = exchange_dir() / "result.json"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = _read_json(path)
        if result and result.get("job_id") == job_id:
            return result
        time.sleep(0.1)
    return None


def ping(timeout=3.0):
    """Ask Grasshopper whether it is listening. Returns its answer or raises BridgeError."""
    result = wait(send("ping"), timeout)
    if result is None:
        raise BridgeError(f"No answer from Grasshopper within {timeout:g} s. {HINT}")
    return result


def generate(system, params, run_dir, timeout=30.0):
    """Have Grasshopper build a design; it writes geometry.json into run_dir."""
    result = wait(send("generate", system, params, run_dir), timeout)
    if result is None:
        raise BridgeError(f"Grasshopper did not answer within {timeout:g} s. {HINT}")
    if result.get("status") != "ok":
        raise BridgeError(result.get("message") or "Grasshopper reported an error.")
    return result
