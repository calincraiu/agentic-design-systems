"""The course app: slides with live widgets that run the real course tools.

Plumbing. You don't need to read this to take the course.
  - The content (what the slides say) is in slides/, as Markdown.
  - The tools the widgets run are in kits/, exactly as students copy them.
  - The widgets themselves are in app/static/app.js.

Start it with:  uv run course
"""
import argparse
import io
import json
import os
import re
import socket
import subprocess
import sys
import threading
import webbrowser
import zipfile
from html import escape
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides"
KITS = ROOT / "kits"
RUNS = ROOT / "runs"
DICE = KITS / "dice" / "tools" / "dice.py"
TOWER = KITS / "tower" / "tools" / "tower" / "tower.py"
READABLE = [KITS, SLIDES, ROOT / "CLAUDE.md", ROOT / "README.md"]

sys.path.insert(0, str(TOWER.parent))
import tower  # noqa: E402  (only to read its parameter and metric lists)

app = FastAPI(title="Agentic Design Systems")
app.mount("/static", StaticFiles(directory=ROOT / "app" / "static"), name="static")
RUNS.mkdir(exist_ok=True)
app.mount("/runs", StaticFiles(directory=RUNS), name="runs")


# SLIDES ----------------------------------------------------------------------


def title_of(text, fallback):
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match[1].strip() if match else fallback


def render(text):
    """Markdown to HTML. {{COURSE_DIR}} becomes this folder's full path, for copy-prompts."""
    text = text.replace("{{COURSE_DIR}}", str(ROOT))
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])


def decks():
    return sorted(p.name for p in SLIDES.iterdir() if p.is_dir()) if SLIDES.exists() else []


def deck_slides(deck):
    folder = SLIDES / deck
    if deck not in decks():
        raise HTTPException(404, f"No slides called '{deck}'")
    files = sorted(folder.glob("*.md"))
    return [{"file": f.name, "text": f.read_text(encoding="utf-8")} for f in files]


def pretty(name):
    return re.sub(r"^\d+-", "", name).replace("-", " ").capitalize()


def page(title, body, mode="read", nav=""):
    return HTMLResponse(SHELL.replace("__TITLE__", escape(title)).replace("__MODE__", mode)
                        .replace("__NAV__", nav).replace("__BODY__", body))


@app.get("/", response_class=HTMLResponse)
def index():
    items = "".join(f'<li><a href="/d/{d}/1">{escape(pretty(d))}</a> · <a href="/d/{d}/read">read as a page</a></li>'
                    for d in decks())
    refs = "".join(f'<li><a href="/p/{p.stem}">{escape(title_of(p.read_text(encoding="utf-8"), pretty(p.stem)))}</a></li>'
                   for p in sorted(SLIDES.glob("*.md")))
    body = (f'<section class="doc"><h1>Agentic Design Systems</h1>'
            f'<p class="lede">The course app. Arrow keys move between slides; <kbd>R</kbd> switches to reading mode.</p>'
            f'<h2>Sessions</h2><ul class="links">{items}</ul>'
            f'<h2>Reference</h2><ul class="links">{refs}</ul></section>')
    return page("Agentic Design Systems", body)


@app.get("/d/{deck}")
def deck_start(deck: str):
    return RedirectResponse(f"/d/{deck}/1")


@app.get("/d/{deck}/read", response_class=HTMLResponse)
def deck_read(deck: str):
    slides = deck_slides(deck)
    body = "".join(f'<section class="doc" id="s{i}">{render(s["text"])}</section>' for i, s in enumerate(slides, 1))
    nav = f'<a href="/">Index</a><span>{escape(pretty(deck))}</span><a href="/d/{deck}/1" data-key="r">Slides</a>'
    return page(pretty(deck), body, "read", nav)


@app.get("/d/{deck}/{n}", response_class=HTMLResponse)
def deck_slide(deck: str, n: int):
    slides = deck_slides(deck)
    if not 1 <= n <= len(slides):
        raise HTTPException(404, f"There is no slide {n}")
    s = slides[n - 1]
    prev_link = f'<a href="/d/{deck}/{n - 1}" data-key="prev">←</a>' if n > 1 else '<span></span>'
    next_link = f'<a href="/d/{deck}/{n + 1}" data-key="next">→</a>' if n < len(slides) else '<span></span>'
    nav = (f'<a href="/">Index</a><span>{escape(pretty(deck))} · {n} / {len(slides)}</span>'
           f'{prev_link}{next_link}<a href="/d/{deck}/read#s{n}" data-key="r">Read</a>')
    progress = f'<div class="progress" style="--p:{n / len(slides):.3f}"></div>'
    body = f'{progress}<section class="slide">{render(s["text"])}</section>'
    return page(title_of(s["text"], pretty(deck)), body, "slides", nav)


@app.get("/p/{name}", response_class=HTMLResponse)
def reference(name: str):
    path = SLIDES / f"{name}.md"
    if not re.fullmatch(r"[\w-]+", name) or not path.exists():
        raise HTTPException(404, f"No page called '{name}'")
    text = path.read_text(encoding="utf-8")
    return page(title_of(text, pretty(name)), f'<section class="doc">{render(text)}</section>', "read",
                '<a href="/">Index</a>')


# FILES AND KITS --------------------------------------------------------------


def readable(rel_path):
    path = (ROOT / rel_path).resolve()
    if not any(path == r or path.is_relative_to(r) for r in READABLE) or not path.is_file():
        raise HTTPException(404, f"Can't show '{rel_path}'")
    return path


@app.get("/api/file")
def file(path: str, render_md: bool = False):
    text = readable(path).read_text(encoding="utf-8")
    return {"path": path, "text": text, "html": render(text) if render_md else None}


def kit_files(name):
    folder = KITS / name
    if not re.fullmatch(r"[\w-]+", name) or not folder.is_dir():
        raise HTTPException(404, f"No kit called '{name}'")
    return folder, sorted(p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts)


@app.get("/api/kits/{name}")
def kit(name: str):
    folder, files = kit_files(name)
    prompt = (f'Copy everything inside the folder "{folder}" into this folder, including the hidden .claude folder. '
              f'Keep the same sub-folders. If a file with the same name already exists here, tell me and leave mine alone. '
              f'Then list what you copied.')
    return {"name": name, "folder": str(folder), "files": [p.relative_to(folder).as_posix() for p in files],
            "prompt": prompt, "zip": f"/kits/{name}.zip"}


@app.get("/kits/{name}.zip")
def kit_zip(name: str):
    folder, files = kit_files(name)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(folder).as_posix())
    return Response(buffer.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="{name}-kit.zip"'})


# TOOLS -----------------------------------------------------------------------
# The widgets run the real tool files, in a separate process, exactly as the agent
# does. They use this app's Python, which already has the tools' dependencies; the
# command shown is the one the agent would type in a student's folder.


def shown(args):
    return " ".join(f'"{a}"' if re.search(r'[\s<>|&"]', a) or a == "" else a for a in args)


def run_tool(script, args, display):
    env = {**os.environ, "ADS_RUNS_DIR": str(RUNS), "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8",
                          cwd=ROOT, env=env, timeout=120)
    return {"command": shown(display + args), "stdout": proc.stdout, "stderr": proc.stderr, "code": proc.returncode}


@app.get("/api/dice")
def dice(sides: int = 6, count: int = 1):
    if count > 1000:
        raise HTTPException(400, "At most 1000 dice at a time")
    result = run_tool(DICE, ["--sides", str(sides), "--count", str(count)], ["uv", "run", "tools/dice.py"])
    match = re.search(r"^Rolls:(.*)$", result["stdout"], re.MULTILINE)
    result["rolls"] = [int(n) for n in match[1].split()] if match else []
    return result


@app.get("/api/tower/spec")
def tower_spec():
    return {
        "params": [{"name": p.name, "int": p.kind is int, "low": p.low, "high": p.high, "default": p.default,
                    "unit": p.unit, "meaning": p.meaning} for p in tower.PARAMS],
        "metrics": [{"name": k, "label": m.label, "unit": m.unit, "meaning": m.meaning} for k, m in tower.METRICS.items()],
    }


class TowerRequest(BaseModel):
    params: dict[str, float] = {}
    plot: str = ""
    require: list[str] = []
    label: str = ""
    why: str = ""
    project: str = "Tower explorer"


@app.post("/api/tower")
def build_tower(req: TowerRequest):
    args = []
    for p in tower.PARAMS:
        value = req.params.get(p.name)
        if value is not None and value != p.default:
            args += ["--" + p.name.replace("_", "-"), f"{int(value)}" if p.kind is int else f"{value:g}"]
    if req.plot.strip():
        args += ["--plot", req.plot.strip()]
    for limit in filter(None, (r.strip() for r in req.require)):
        args += ["--require", limit]
    for flag, value in (("--label", req.label), ("--why", req.why), ("--project", req.project)):
        if value.strip():
            args += [flag, value.strip()]
    args += ["--skill", "course app"]
    result = run_tool(TOWER, args, ["uv", "run", "tools/tower/tower.py"])
    match = re.search(r"^Image: (.+)$", result["stdout"], re.MULTILINE)
    if match:
        image = (ROOT / match[1].strip()).resolve()
        result["image"] = "/runs/" + image.relative_to(RUNS).as_posix()
        result["run"] = json.loads((image.parent / "run.json").read_text(encoding="utf-8"))
    return result


# STARTING THE APP ------------------------------------------------------------


def free_port(preferred=8765):
    for port in [preferred, *range(8766, 8800)]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit("No free port between 8765 and 8799. Close another copy of the course app and try again.")


def run():
    import uvicorn

    parser = argparse.ArgumentParser(description="Start the course app and open it in your browser.")
    parser.add_argument("--port", type=int, default=8765, help="Port to try first (default 8765).")
    parser.add_argument("--no-browser", action="store_true", help="Don't open the browser.")
    args = parser.parse_args()
    port = free_port(args.port)
    url = f"http://127.0.0.1:{port}"
    print(f"\n  Course app running at {url}\n  Leave this window open while you use it. Close it (or press Ctrl+C) to stop.\n",
          flush=True)
    if not args.no_browser:
        threading.Timer(1.0, webbrowser.open, [url]).start()
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="/static/app.css">
</head>
<body class="__MODE__">
<nav class="bar">__NAV__</nav>
<main>__BODY__</main>
<script src="/static/app.js"></script>
</body>
</html>
"""
