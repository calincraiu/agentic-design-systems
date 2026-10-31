"""Render stacked floor plates as a small 3D image, with matplotlib (no Rhino needed).

Images are made here rather than captured from Rhino so every run looks the same,
whichever backend produced it, on any computer.
"""
import math

import matplotlib

matplotlib.use("Agg")  # draw to files, never open windows
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

MASS = (0.86, 0.83, 0.79)
EDGE = "#4a4540"
SHADOW = "#56657a"
PLOT = "#b5522b"
LIGHT = (-0.6, -0.8)  # light from the south-west, so those faces read brighter


def _shade(a, b):
    """Brightness of a wall between plan points a and b, from its outward normal."""
    nx, ny = b[1] - a[1], -(b[0] - a[0])  # outward for anticlockwise polygons
    length = math.hypot(nx, ny) or 1.0
    facing = max(0.0, (nx * LIGHT[0] + ny * LIGHT[1]) / length)
    k = 0.62 + 0.38 * facing
    return tuple(c * k for c in MASS)


def render_floors(curves, floor_height, path, plot=None, shadow=None, caption=""):
    """Draw each floor outline extruded by floor_height and save a PNG.

    curves: floors, each a list of [x, y, z] points (z = bottom of the floor)
    plot:   (width, depth) of the site, centred on the origin
    shadow: ground polygon [[x, y], ...]
    """
    fig = plt.figure(figsize=(6, 6), dpi=110)
    ax = fig.add_subplot(projection="3d")

    faces, colors = [], []
    for floor in curves:
        z0 = floor[0][2]
        z1 = z0 + floor_height
        for i in range(len(floor)):
            a, b = floor[i], floor[(i + 1) % len(floor)]
            faces.append([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)])
            colors.append(_shade(a, b))
        faces.append([(p[0], p[1], z1) for p in floor])
        colors.append(MASS)
    ax.add_collection3d(Poly3DCollection(faces, facecolors=colors, edgecolors=EDGE, linewidths=0.3))

    xs = [p[0] for f in curves for p in f]
    ys = [p[1] for f in curves for p in f]
    if shadow:
        ax.add_collection3d(Poly3DCollection([[(x, y, 0) for x, y in shadow]], facecolors=SHADOW, alpha=0.3, edgecolors="none"))
        xs += [p[0] for p in shadow]
        ys += [p[1] for p in shadow]
    if plot:
        w, d = plot[0] / 2, plot[1] / 2
        ax.plot([-w, w, w, -w, -w], [-d, -d, d, d, -d], [0] * 5, color=PLOT, linestyle="--", linewidth=1)
        xs += [-w, w]
        ys += [-d, d]

    top = max(p[2] for f in curves for p in f) + floor_height
    span_x, span_y = max(xs) - min(xs), max(ys) - min(ys)
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.set_zlim(0, top)
    ax.set_box_aspect((max(span_x, 1), max(span_y, 1), max(top, 1)), zoom=1.15)

    # North arrow at the north-west corner of the drawing.
    arrow = max(span_x, span_y) * 0.08
    nx, ny = min(xs), max(ys)
    ax.plot([nx, nx], [ny - arrow, ny], [0, 0], color=EDGE, linewidth=1.2)
    ax.text(nx, ny + arrow * 0.3, 0, "N", color=EDGE, fontsize=9, ha="center")

    ax.view_init(elev=22, azim=-55)
    ax.set_axis_off()
    if caption:
        fig.text(0.04, 0.04, caption, fontsize=13, color=EDGE, family="monospace")
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
