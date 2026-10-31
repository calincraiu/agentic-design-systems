"""Where things live in this repo.

Everything is found relative to the repo root (the folder holding pyproject.toml),
so the kit works wherever the repo is cloned or unzipped, on Windows or Mac.
"""
import os
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for folder in here.parents:
        if (folder / "pyproject.toml").exists():
            return folder
    raise RuntimeError("Could not find the repo root (no pyproject.toml above kit/).")


ROOT = repo_root()


def runs_dir() -> Path:
    """One folder per design run. Overridable (ADS_RUNS_DIR) so tests stay out of runs/."""
    return Path(os.environ.get("ADS_RUNS_DIR", ROOT / "runs"))


def exchange_dir() -> Path:
    """The mailbox folder shared with Grasshopper (job.json in, result.json out)."""
    return Path(os.environ.get("ADS_EXCHANGE_DIR", ROOT / ".exchange"))


def rel(path) -> str:
    """A path relative to the repo root, with forward slashes, for readable output."""
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()
