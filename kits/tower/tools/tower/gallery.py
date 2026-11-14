"""Plumbing: run folders, and the page that compares them. You don't need to read this.

runs/<run_id>/
  run.json       label, skill, reason ("why"), parameters, metrics and limit checks
  geometry.json  the floor outlines the generator produced
  image.png      a rendered view
runs/gallery.html  every run, grouped by project. Rebuilt after every run.

Run it directly to rebuild the page: uv run tools/gallery.py --open
"""
import argparse
import json
import os
import re
import webbrowser
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def runs_dir():
    """One folder per design run. Overridable (ADS_RUNS_DIR) so tests stay out of runs/."""
    return Path(os.environ.get("ADS_RUNS_DIR", ROOT / "runs"))


def rel(path):
    """A path relative to the repo root, with forward slashes, for readable output."""
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def new_run(label):
    """Create and return an empty, uniquely named run folder."""
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:40].strip("-")
    base = "-".join(filter(None, [datetime.now().strftime("%Y%m%d-%H%M%S"), slug]))
    folder = runs_dir() / base
    n = 2
    while folder.exists():
        folder = runs_dir() / f"{base}-{n}"
        n += 1
    folder.mkdir(parents=True)
    return folder


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def list_runs():
    """Every complete run, oldest first."""
    if not runs_dir().exists():
        return []
    runs = []
    for folder in sorted(p for p in runs_dir().iterdir() if p.is_dir()):
        if (folder / "run.json").exists():
            runs.append({"id": folder.name, **json.loads((folder / "run.json").read_text(encoding="utf-8"))})
    return runs


def fmt(value):
    if value is None:
        return "–"
    return f"{value:,.0f}" if abs(value) >= 100 else f"{value:.4g}"


def table(runs):
    keys = list(runs[0]["headings"])
    head = "".join(f"<th>{escape(runs[0]['headings'][k])}</th>" for k in keys)
    rows = []
    for r in runs:
        failed = {c["metric"] for c in r["limits"] if c["pass"] is False}
        cells = "".join(f'<td{" class=fail" if k in failed else ""}>{fmt(r["metrics"].get(k))}</td>' for k in keys)
        rows.append(f"<tr><td>{escape(r['label'])}</td><td>{escape(r['skill'])}</td>{cells}</tr>")
    return f'<div class="wrap"><table><tr><th>Variant</th><th>Skill</th>{head}</tr>{"".join(rows)}</table></div>'


def card(r):
    checks = "".join(
        f'<li class="{"pass" if c["pass"] else "fail"}">{"✓" if c["pass"] else "✗"} '
        f'{escape(c["metric"])} {escape(c["op"])} {c["value"]:g} (actual {fmt(c["actual"])})</li>'
        for c in r["limits"])
    params = "".join(f"<dt>{escape(k)}</dt><dd>{v:g}</dd>" for k, v in r["params"].items())
    why = f'<p class="why">{escape(r["why"])}</p>' if r["why"] else ""
    return (f'<article><img src="{escape(r["id"])}/image.png" alt="{escape(r["label"])}">'
            f'<h3>{escape(r["label"])}</h3><p class="skill">{escape(r["skill"])}</p>{why}'
            f'<ul>{checks}</ul><details><summary>Parameters</summary><dl>{params}</dl></details></article>')


def build(open_browser=False):
    """Write runs/gallery.html. Newest project first; runs in the order they were made."""
    runs = list_runs()
    groups = {}
    for r in runs:
        groups.setdefault(r["project"] or "No project", []).append(r)
    sections = "".join(
        f'<section><h2>{escape(name)}</h2>{table(group)}<div class="grid">{"".join(card(r) for r in group)}</div></section>'
        for name, group in reversed(groups.items()))
    count = f"{len(runs)} run{'' if len(runs) == 1 else 's'}"
    page = (TEMPLATE.replace("__COUNT__", count)
            .replace("__SECTIONS__", sections or "<p>No runs yet. Generate a design and refresh this page.</p>"))
    path = runs_dir() / "gallery.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")
    if open_browser:
        webbrowser.open(path.resolve().as_uri())
    return path


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Design Runs</title>
<style>
:root {
  --bg: #f6f4f0; --surface: #ffffff; --ink: #24211e; --muted: #6f6a63; --line: #e2ddd5;
  --accent: #b5522b; --pass: #2f7d4f; --fail: #b3261e;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #171614; --surface: #211f1c; --ink: #ece8e1; --muted: #a39d94; --line: #36322d;
    --accent: #e0835a; --pass: #6cc28f; --fail: #f08a80;
  }
}
* { box-sizing: border-box; }
body { margin: 0 auto; padding: 24px 16px 48px; max-width: 1400px; background: var(--bg); color: var(--ink); font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
h1 { margin: 0; font-size: 22px; }
.sub { margin: 4px 0 0; color: var(--muted); }
section { margin-top: 28px; }
h2 { margin: 0 0 12px; padding-bottom: 6px; font-size: 16px; border-bottom: 1px solid var(--line); }
.wrap { overflow-x: auto; margin-bottom: 14px; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
table { width: 100%; border-collapse: collapse; font-size: 12px; font-variant-numeric: tabular-nums; }
th, td { padding: 6px 10px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
th:nth-child(-n+2), td:nth-child(-n+2) { text-align: left; }
th { color: var(--muted); font-weight: 600; }
td.fail { color: var(--fail); font-weight: 600; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
article { padding-bottom: 12px; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
article > :not(img) { margin-left: 12px; margin-right: 12px; }
img { display: block; width: 100%; aspect-ratio: 1; object-fit: contain; background: #fff; }
h3 { margin-top: 10px; margin-bottom: 0; font-size: 15px; }
.skill { margin-top: 2px; margin-bottom: 6px; color: var(--accent); font-size: 12px; }
.why { margin-top: 0; margin-bottom: 6px; color: var(--muted); font-style: italic; }
ul { padding: 0; margin-top: 0; margin-bottom: 6px; list-style: none; font-size: 12px; }
.pass { color: var(--pass); } .fail { color: var(--fail); }
summary { color: var(--muted); font-size: 12px; cursor: pointer; }
dl { display: grid; grid-template-columns: 1fr auto; gap: 1px 10px; margin: 4px 0 0; font-size: 12px; }
dt { color: var(--muted); } dd { margin: 0; text-align: right; }
</style>
</head>
<body>
<h1>Design runs</h1>
<p class="sub">__COUNT__ · refresh this page after new runs</p>
__SECTIONS__
</body>
</html>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild runs/gallery.html.")
    parser.add_argument("--open", action="store_true", help="Also open it in your browser.")
    print(f"Gallery: {rel(build(open_browser=parser.parse_args().open))}")
