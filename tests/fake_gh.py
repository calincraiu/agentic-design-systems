"""A stand-in for Grasshopper that speaks the bridge protocol, for tests.

It answers jobs the way kit/gh/listener.py and kit/gh/writer.py do, using the
Python tower generator instead of the Grasshopper definition.
"""
import json
import threading
import time
from pathlib import Path

from examples.tower.generate import build


class FakeGrasshopper:
    def __init__(self, exchange, system="tower", active=True):
        self.exchange = Path(exchange)
        self.system = system
        self.active = active
        self._stop = threading.Event()
        self._seen = None
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join(timeout=2)

    def _answer(self, job, status, message, **extra):
        result = {"job_id": job["job_id"], "status": status, "message": message, **extra}
        (self.exchange / "result.json").write_text(json.dumps(result), encoding="utf-8")

    def _loop(self):
        while not self._stop.is_set():
            time.sleep(0.05)
            try:
                job = json.loads((self.exchange / "job.json").read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if job["job_id"] == self._seen:
                continue
            self._seen = job["job_id"]
            if job["kind"] == "ping":
                self._answer(job, "pong", "listening", system=self.system, active=self.active, rhino="fake")
            elif job["system"] != self.system:
                self._answer(job, "error", f"This Grasshopper definition is '{self.system}'.")
            elif not self.active:
                self._answer(job, "error", "Agent control is OFF in Grasshopper.")
            else:
                geometry = build(job["params"])
                geometry["source"] = "grasshopper"
                (Path(job["run_dir"]) / "geometry.json").write_text(json.dumps(geometry), encoding="utf-8")
                self._answer(job, "ok", "sent")
