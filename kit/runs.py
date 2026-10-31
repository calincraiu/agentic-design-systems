"""Run folders: one folder per design attempt, holding everything about it.

runs/<run_id>/
  meta.json      label, skill, brief, backend, time and the agent's reason ("why")
  brief.json     snapshot of the structured brief used (if any)
  params.json    the parameters sent to the generator
  geometry.json  what the generator produced
  metrics.json   what the evaluator measured, plus constraint checks
  image.png      a rendered view

Together, the run folders are the design diary of the project.
"""
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from .paths import runs_dir


def slugify(text, max_len=40):
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return slug[:max_len].strip("-")


def new_run(label=""):
    """Create and return an empty, uniquely named run folder."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = f"{stamp}-{slugify(label)}" if slugify(label) else stamp
    folder = runs_dir() / base
    n = 2
    while folder.exists():
        folder = runs_dir() / f"{base}-{n}"
        n += 1
    folder.mkdir(parents=True)
    return folder


def discard(folder):
    """Remove a run that failed, so it doesn't clutter the gallery."""
    shutil.rmtree(folder, ignore_errors=True)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def list_runs():
    """Every complete run, oldest first."""
    root = runs_dir()
    if not root.exists():
        return []
    runs = []
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        if not (folder / "meta.json").exists() or not (folder / "metrics.json").exists():
            continue
        runs.append({
            "id": folder.name,
            "meta": read_json(folder / "meta.json"),
            "params": read_json(folder / "params.json") if (folder / "params.json").exists() else {},
            "metrics": read_json(folder / "metrics.json"),
            "image": f"{folder.name}/image.png" if (folder / "image.png").exists() else None,
        })
    return runs
