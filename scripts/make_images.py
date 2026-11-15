"""Make the pictures the slides use, by running the real tower tool.

  uv run scripts/make_images.py

Writes:
  app/static/img/*.png         eight contrasting towers, for the contact sheet on the hook slide
  slides/figures/skyline.svg   a skyline in elevation, drawn from the tower's own geometry (title slide)

Both are committed, so nobody needs to run this unless the tower tool changes.
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kits" / "tower" / "tools" / "tower"))

import gallery  # noqa: E402
import tower  # noqa: E402

IMG = ROOT / "app" / "static" / "img"

# name, label, parameters: eight different answers to "make a tower"
SHEET = [
    ("slim-beacon", "A: slim beacon", dict(floors=60, width=14, depth=14, taper=0.6)),
    ("quarter-turn", "B: quarter turn", dict(floors=40, width=24, depth=24, twist=90, taper=0.8)),
    ("squat-block", "C: squat block", dict(floors=12, width=40, depth=40)),
    ("leaning", "D: leaning east", dict(floors=30, width=22, depth=22, lean=14, lean_dir=90, taper=0.9)),
    ("flared-top", "E: flared top", dict(floors=30, width=16, depth=16, taper=1.6)),
    ("long-slab", "F: long slab", dict(floors=25, width=50, depth=12)),
    ("full-turn", "G: full turn", dict(floors=50, width=20, depth=20, twist=360, taper=0.7)),
    ("needle", "H: needle", dict(floors=70, floor_height=3.2, width=9, depth=9)),
]

# the skyline: four towers side by side, and which one is picked out in terracotta
SKYLINE = [
    (dict(floors=24, floor_height=3.6, width=26, depth=26), False),
    (dict(floors=60, floor_height=3.5, width=16, depth=16, twist=140, taper=0.55), True),
    (dict(floors=36, floor_height=3.5, width=22, depth=22, lean=12, lean_dir=90, taper=0.8), False),
    (dict(floors=16, floor_height=4.0, width=40, depth=14, taper=1.4), False),
]


def contact_sheet():
    IMG.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["ADS_RUNS_DIR"] = str(Path(tmp) / "runs")
        for name, label, params in SHEET:
            args = ["--label", label, "--project", "Contact sheet", "--skill", "make_images"]
            for key, value in params.items():
                args += ["--" + key.replace("_", "-"), str(value)]
            with contextlib.redirect_stdout(io.StringIO()):
                assert tower.main(args) == 0, name
            run = gallery.list_runs()[-1]
            shutil.copy(Path(tmp) / "runs" / run["id"] / "image.png", IMG / f"{name}.png")
            print("wrote", name)


def skyline():
    towers = []
    for params, picked in SKYLINE:
        g = tower.build(params)
        xs = [p[0] for floor in g["curves"] for p in floor]
        towers.append((g, min(xs), max(xs), picked))
    gap = 12
    x = 0
    placed = []
    for g, lo, hi, picked in towers:
        placed.append((g, x - lo, picked))
        x += hi - lo + gap
    total_w = x - gap
    total_h = max(len(g["curves"]) * g["floor_height"] for g, *_ in towers)
    margin = 8
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-margin} {-margin} {total_w + 2 * margin:.1f} {total_h + 2 * margin:.1f}" '
           'role="img" aria-label="A skyline of four different towers, drawn in elevation" preserveAspectRatio="xMidYMax meet">']
    for g, dx, picked in placed:
        fh = g["floor_height"]
        style = ' style="stroke:var(--accent);stroke-width:1.5"' if picked else ""
        out.append(f'  <g class="hair"{style}>')
        for i, floor in enumerate(g["curves"]):
            xs = [p[0] + dx for p in floor]
            y_top = total_h - (i + 1) * fh
            out.append(f'    <rect x="{min(xs):.2f}" y="{y_top:.2f}" width="{max(xs) - min(xs):.2f}" height="{fh:.2f}"/>')
        out.append("  </g>")
    out.append(f'  <line class="ink" x1="{-margin}" y1="{total_h:.1f}" x2="{total_w + margin:.1f}" y2="{total_h:.1f}" style="vector-effect:non-scaling-stroke"/>')
    out.append("</svg>")
    target = ROOT / "slides" / "figures" / "skyline.svg"
    target.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("wrote", target.relative_to(ROOT))


if __name__ == "__main__":
    contact_sheet()
    skyline()
