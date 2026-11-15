"""Generates slides/figures/loop.svg: the design loop as a ring of five steps, coloured by who does each one.

  uv run scripts/make_loop.py

The SVG is plain text and can also be edited by hand; this script just does the arrow geometry."""
import math
from pathlib import Path

CX, CY, R = 320, 290, 215
W, H = 200, 54
NODES = [  # label, kind. You are the client: you say what you want, and you choose.
    ("You describe", "you"),
    ("Agent asks", "agent"),
    ("You answer", "you"),
    ("Tool builds three", "tool"),
    ("Report; you choose", "you"),
]
N = len(NODES)
CLASS = {"agent": "box-accent", "tool": "box-blue", "you": "ink-fill"}


def centre(k):
    a = math.radians(-90 + 360 / N * k)
    return CX + R * math.cos(a), CY + R * math.sin(a)


def clip(p, q, gap=8):
    """Point on the boundary of the node box at p, on the line towards q, pushed out by gap."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = min((W / 2) / abs(dx) if dx else 1e9, (H / 2) / abs(dy) if dy else 1e9)
    n = math.hypot(dx, dy)
    return p[0] + dx * t + dx / n * gap, p[1] + dy * t + dy / n * gap


out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 590" role="img" aria-label="The design loop: you describe, the agent asks, you answer, the tool builds and measures three, you choose, then round again">',
       '  <defs><marker id="loop-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" class="ah-ink"/></marker></defs>']
pts = [centre(k) for k in range(N)]
for k, (label, kind) in enumerate(NODES):
    x, y = pts[k]
    prev = pts[k - 1]
    a, b = clip(prev, (x, y)), clip((x, y), prev)
    # the arrow into this node appears with it; the last one closes the loop
    step = k + 1
    if k > 0:
        out.append(f'  <line class="ink" data-step="{step}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" marker-end="url(#loop-ink)"/>')
    text_class = "paper-text" if kind == "you" else ""
    out.append(f'  <g data-step="{step}"><rect class="{CLASS[kind]}" x="{x - W / 2:.1f}" y="{y - H / 2:.1f}" width="{W}" height="{H}"/>'
               f'<text class="{text_class}" x="{x:.1f}" y="{y + 7:.1f}" text-anchor="middle">{label}</text></g>')
# closing arrow, last node back to the first, once the whole loop is on show
a, b = clip(pts[-1], pts[0]), clip(pts[0], pts[-1])
out.append(f'  <line class="accent" data-step="{N + 1}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" marker-end="url(#loop-ink)" style="stroke-dasharray:8 6"/>')
out.append(f'  <g data-step="{N + 1}"><text class="small" x="{CX}" y="{CY - 8}" text-anchor="middle">Not happy?</text>'
           f'<text class="small" x="{CX}" y="{CY + 16}" text-anchor="middle">Change the brief,</text>'
           f'<text class="small" x="{CX}" y="{CY + 40}" text-anchor="middle">the skill or the tool.</text></g>')
# legend, always visible
legend = [("agent", "box-accent", 70), ("tool", "box-blue", 230), ("you", "ink-fill", 390)]
for name, cls, x in legend:
    out.append(f'  <rect class="{cls}" x="{x}" y="560" width="22" height="16"/><text class="label" x="{x + 32}" y="573">{name}</text>')
out.append("</svg>")
(Path(__file__).resolve().parents[1] / "slides" / "figures" / "loop.svg").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
print("ok")
