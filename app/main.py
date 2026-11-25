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
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides"
KITS = ROOT / "kits"
RUNS = ROOT / "runs"
ADD = KITS / "add" / "tools" / "add.py"
DICE = KITS / "dice" / "tools" / "dice.py"
TOWER = KITS / "tower" / "tools" / "tower" / "tower.py"
READABLE = [KITS, SLIDES, ROOT / "CLAUDE.md", ROOT / "README.md"]

sys.path.insert(0, str(TOWER.parent))
import tower  # noqa: E402  (only to read its parameter and metric lists)

app = FastAPI(title="Agentic Design Systems")


@app.middleware("http")
async def no_stale_assets(request, call_next):
    """The course files change while the course is built: make the browser re-check app.js and app.css every time."""
    response = await call_next(request)
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache"
    return response


app.mount("/static", StaticFiles(directory=ROOT / "app" / "static"), name="static")
RUNS.mkdir(exist_ok=True)
app.mount("/runs", StaticFiles(directory=RUNS), name="runs")


# SLIDES ----------------------------------------------------------------------

# Where the student is working while a slide is up. Shown as a chip in the slide's title block.
WHERE = {
    "chat": "Chat tab",
    "code-yours": "Code tab · your folder",
    "code-course": "Code tab · course folder",
    "rhino": "Rhino · Grasshopper",
    "app": "This app",
}
LAYOUTS = {"title", "section", "statement", "stage", "split", "diagram", "task", "outline"}


def title_of(text, fallback):
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match[1].strip() if match else fallback


def render(text):
    """Markdown to HTML. {{COURSE_DIR}} becomes this folder's full path, for copy-prompts."""
    text = text.replace("{{COURSE_DIR}}", str(ROOT))
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])


def split_slide(text):
    """Split one slide's Markdown into its settings, the slide itself and its speaker notes.

    Line 1 may be a comment with settings, separated by bars:
        <!-- layout: task | where: code-yours | time: 25 min | pairs -->
    Everything after a line that says  <!-- notes -->  is speaker notes: hidden on the
    projector until the student presses N.
    """
    meta = {"layout": "stage", "where": None, "time": None, "pairs": False}
    first = re.match(r"\s*<!--(.*?)-->[ \t]*\n?", text, re.DOTALL)
    if first and first[1].strip() != "notes":
        for item in first[1].split("|"):
            key, _, value = item.partition(":")
            if key.strip():
                meta[key.strip()] = value.strip() or True
        text = text[first.end():]
    if meta["layout"] not in LAYOUTS:
        meta["layout"] = "stage"
    if meta["where"] not in WHERE:
        meta["where"] = None
    parts = re.split(r"^<!--\s*notes\s*-->[ \t]*$", text, maxsplit=1, flags=re.MULTILINE)
    body, notes = parts[0], (parts[1] if len(parts) > 1 else "")
    return {**meta, "body": body.strip(), "notes": notes.strip(), "title": title_of(body, "")}


def decks():
    if not SLIDES.exists():
        return []
    return sorted(p.name for p in SLIDES.iterdir() if p.is_dir() and any(p.glob("*.md")))


def deck_slides(deck):
    folder = SLIDES / deck
    if deck not in decks():
        raise HTTPException(404, f"No slides called '{deck}'")
    slides = []
    for f in sorted(folder.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        slides.append({"file": f.name, "text": text, **split_slide(text)})
    return slides


def pretty(name):
    return re.sub(r"^\d+-", "", name).replace("-", " ").capitalize()


def chip(where):
    return f'<span class="chip where-{where}">{escape(WHERE[where])}</span>' if where else ""


def badges(s, with_chip=True):
    items = [chip(s["where"]) if with_chip else ""]
    if s["time"]:
        items.append(f'<span class="badge">{escape(str(s["time"]))}</span>')
    if s["pairs"]:
        items.append('<span class="badge">in pairs</span>')
    return "".join(i for i in items if i)


KEYS_BUTTON = '<button type="button" class="keys-btn" data-keys title="Keyboard shortcuts (?)">? Keys</button>'


def page(title, body, mode="read", nav=""):
    return HTMLResponse(SHELL.replace("__TITLE__", escape(title)).replace("__MODE__", mode)
                        .replace("__NAV__", nav + KEYS_BUTTON).replace("__BODY__", body))


@app.get("/", response_class=HTMLResponse)
def index():
    cards = []
    for d in decks():
        slides = deck_slides(d)
        number = re.search(r"\d+", d)
        chapters = "".join(f"<li>{escape(s['title'])}</li>" for s in slides if s["layout"] == "section")
        chapters = f'<ul class="chapters">{chapters}</ul>' if chapters else ""
        cards.append(
            f'<article class="session"><p class="kicker">Session {number[0] if number else ""}</p>'
            f'<h3>{escape(pretty(d))}</h3>'
            f'<p class="muted">{len(slides)} slides</p>{chapters}'
            f'<p class="actions"><a class="btn primary" href="/d/{d}/1">Open slides →</a>'
            '</p></article>')
    refs = "".join(f'<a class="ref" href="/p/{p.stem}"><span>{escape(title_of(p.read_text(encoding="utf-8"), pretty(p.stem)))}</span>'
                   f'<span class="arrow">→</span></a>' for p in sorted(SLIDES.glob("*.md")))
    keys = [("← →", "Move between slides"), ("N", "More on this slide"), ("G", "See all slides"),
            ("D", "Dark mode"), ("F", "Full screen"), ("?", "All shortcuts")]
    keys = "".join(f"<div><kbd>{k}</kbd><span>{escape(v)}</span></div>" for k, v in keys)
    body = (
        '<div class="home">'
        '<header class="hero-band"><div class="hero-text">'
        '<p class="rc5"><span>RC5</span> Research Cluster 5</p>'
        '<h1>Agentic Design Systems</h1>'
        '<p class="tagline">From asking an AI for a design to building the system it works inside.</p>'
                '<p class="facts"><span>Masters module · 12 hours</span></p>'
        '</div><div class="hero-art"><div data-widget="figure" data-name="skyline" class="hero"></div></div></header>'
        f'<section id="sessions"><h2 class="band">Sessions</h2><div class="session-grid">{"".join(cards)}</div></section>'
        '<section><h2 class="band">Reference</h2>'
        f'<p class="muted">Short pages to come back to between sessions.</p><div class="ref-grid">{refs}</div></section>'
        f'<section><h2 class="band">Find your way around</h2><div class="keys-grid">{keys}</div></section>'
        '<footer class="home-foot">RC5 · Agentic Design Systems</footer></div>')
    return page("Agentic Design Systems · RC5", body)


@app.get("/d/{deck}")
def deck_start(deck: str):
    return RedirectResponse(f"/d/{deck}/1")


@app.get("/api/deck/{deck}")
def deck_outline(deck: str):
    return [{"n": i, "title": s["title"] or pretty(s["file"].removesuffix(".md")), "layout": s["layout"], "where": s["where"], "notes": bool(s["notes"])}
            for i, s in enumerate(deck_slides(deck), 1)]


@app.get("/d/{deck}/{n}", response_class=HTMLResponse)
def deck_slide(deck: str, n: int):
    slides = deck_slides(deck)
    if not 1 <= n <= len(slides):
        raise HTTPException(404, f"There is no slide {n}")
    s = slides[n - 1]
    prev_link = f'<a href="/d/{deck}/{n - 1}" data-key="prev" title="Previous slide (←)">← Back</a>' if n > 1 else "<span></span>"
    next_link = f'<a href="/d/{deck}/{n + 1}" data-key="next" title="Next slide (→)">Next →</a>' if n < len(slides) else "<span></span>"
    nav = (f'<a href="/">Index</a><span>{escape(pretty(deck))}</span>'
           f'{prev_link}{next_link}')
    progress = f'<div class="progress" style="--p:{n / len(slides):.3f}"></div>'
    extra = f'<div class="badges">{badges(s, with_chip=False)}</div>' if s["layout"] == "task" else ""
    notes = (f'<aside id="notes" class="notes" hidden><div class="notes-head"><h4>More on this slide</h4><button type="button" class="notes-close" data-notes-close>Close ✕</button></div>{render(s["notes"])}</aside>'
             if s["notes"] else "")
    notes_btn = ('<button type="button" class="notes-btn" data-notes aria-controls="notes" aria-expanded="false" '
                 'title="Study notes (N)">✎ Notes <kbd>N</kbd></button>' if s["notes"] else "")
    block = (f'<footer class="titleblock"><span>ADS · {escape(pretty(deck))}</span>'
             f'<strong>{escape(s["title"])}</strong><span>{n:02d} / {len(slides):02d}</span>{notes_btn}{chip(s["where"])}</footer>')
    body = (f'{progress}<div class="sheet"><section class="slide layout-{s["layout"]}">{extra}{render(s["body"])}</section>'
            f'{block}</div>{notes}<div id="deck" data-deck="{escape(deck)}" data-n="{n}"></div>')
    return page(s["title"] or pretty(deck), body, "slides", nav)


@app.get("/p/{name}", response_class=HTMLResponse)
def reference(name: str):
    path = SLIDES / f"{name}.md"
    if not re.fullmatch(r"[\w-]+", name) or not path.exists():
        raise HTTPException(404, f"No page called '{name}'")
    text = path.read_text(encoding="utf-8")
    return page(title_of(text, pretty(name)), f'<section class="doc">{render(text)}</section>', "read",
                '<a href="/">Index</a>')


@app.get("/api/figure/{name}")
def figure(name: str):
    path = SLIDES / "figures" / f"{name}.svg"
    if not re.fullmatch(r"[\w-]+", name) or not path.is_file():
        raise HTTPException(404, f"No figure called '{name}'")
    return Response(path.read_text(encoding="utf-8"), media_type="image/svg+xml")


# FILES AND KITS --------------------------------------------------------------


def readable(rel_path):
    path = (ROOT / rel_path).resolve()
    if not any(path == r or path.is_relative_to(r) for r in READABLE) or not path.is_file():
        raise HTTPException(404, f"Can't show '{rel_path}'")
    return path


@app.get("/api/file")
def file(path: str, render_md: bool = False):
    text = readable(path).read_text(encoding="utf-8")
    return {"path": path, "text": text, "html": render(blank_line_before_lists(text)) if render_md else None}


def blank_line_before_lists(text):
    """Markdown only starts a list after a blank line, and hand-written notes often don't leave one."""
    return re.sub(r"^([^\n-][^\n]*)\n(- )", r"\1\n\n\2", text, flags=re.MULTILINE)


def kit_files(names):
    """One kit ("dice") or several, separated by commas ("add,dice"). Returns [(folder, files), ...]."""
    found = []
    for name in names.split(","):
        folder = KITS / name.strip()
        if not re.fullmatch(r"[\w-]+", name.strip()) or not folder.is_dir():
            raise HTTPException(404, f"No kit called '{name}'")
        skip = {"__pycache__", "runs"}  # runs/: receipts from running a tool inside the kit
        found.append((folder, sorted(p for p in folder.rglob("*") if p.is_file() and not skip & set(p.relative_to(folder).parts))))
    return found


def kit_prompt(folders):
    """The copy-prompt. The paths are found on the computer the app runs on, so each student's own app
    shows their own paths: that's why students copy it from their app, not from the projector."""
    where = " and ".join(f'"{f}"' for f in folders)
    many = len(folders) > 1
    return (f'Copy everything inside {"these folders" if many else "this folder"}: {where}, into the folder I have open, '
            f'including the hidden .claude folder. Keep the same sub-folders. '
            f"{'They are' if many else 'It is'} in the course folder on this computer. "
            f"If {'they don' if many else 'it doesn'}'t exist, stop and ask me where I unzipped the course folder. "
            f'If a file with the same name is already here and identical, skip it; '
            f'if it is different, tell me and leave mine alone. Then list what you copied.')


@app.get("/api/kits/{names}")
def kit(names: str):
    kits = kit_files(names)
    files = sorted({p.relative_to(folder).as_posix() for folder, ps in kits for p in ps})
    return {"name": " + ".join(f.name for f, _ in kits), "folder": [str(f) for f, _ in kits], "files": files,
            "prompt": kit_prompt([f for f, _ in kits]), "zip": f"/kits/{names}.zip"}


@app.get("/kits/{names}.zip")
def kit_zip(names: str):
    name = names.replace(",", "-")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        written = set()
        for folder, files in kit_files(names):
            for p in files:
                arc = p.relative_to(folder).as_posix()
                if arc not in written:  # every kit's .claude/settings.json is the same
                    z.write(p, arc)
                    written.add(arc)
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


@app.get("/api/add")
def add(numbers: str = "2 2"):
    values = numbers.split()
    if not 1 <= len(values) <= 200:
        raise HTTPException(400, "Give between 1 and 200 numbers")
    result = run_tool(ADD, values, ["uv", "run", "tools/add.py"])
    match = re.search(r"^Total: (.+)$", result["stdout"], re.MULTILINE)
    result["total"] = match[1].strip() if match else None
    return result


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


@app.get("/api/tower/preview")
def tower_preview(request: Request):
    """Floor outlines straight from the tower's own build(), with no drawing: fast enough for a live preview."""
    try:
        geometry = tower.build({k: float(v) for k, v in request.query_params.items()})
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"curves": [[[x, y] for x, y, _ in floor] for floor in geometry["curves"]], "floor_height": geometry["floor_height"]}


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
<script>try{var q=new URLSearchParams(location.search).get("theme");if(q==="light"||q==="dark")localStorage.setItem("ads-theme",q);var t=localStorage.getItem("ads-theme");if(t)document.documentElement.dataset.theme=t}catch(e){var q2=new URLSearchParams(location.search).get("theme");if(q2)document.documentElement.dataset.theme=q2}</script>
<link rel="stylesheet" href="/static/app.css">
</head>
<body class="__MODE__">
<nav class="bar">__NAV__</nav>
<main>__BODY__</main>
<script src="/static/app.js"></script>
</body>
</html>
"""
