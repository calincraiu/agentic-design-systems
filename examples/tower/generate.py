"""The Python generator: builds the same tower as tower.gh, without Rhino.

For each floor i, with t = i / (floors - 1) running from 0 (ground) to 1 (top):
  1. start from a width x depth rectangle centred on the origin
  2. scale it by 1 + (taper - 1) * t
  3. rotate it by twist * t degrees
  4. move it by lean * t towards lean_dir, and up to z = i * floor_height

The result has the same shape as the geometry.json the Grasshopper Writer sends back.
"""
import math

from kit.geometry import rectangle

from . import SYSTEM
from .params import resolve


def build(params):
    p = resolve(params)
    n = p["floors"]
    base = rectangle(p["width"], p["depth"])
    heading = math.radians(p["lean_dir"])
    curves = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.0
        scale = 1 + (p["taper"] - 1) * t
        angle = math.radians(p["twist"] * t)
        dx = p["lean"] * t * math.sin(heading)
        dy = p["lean"] * t * math.cos(heading)
        z = i * p["floor_height"]
        floor = []
        for x, y in base:
            x, y = x * scale, y * scale
            x, y = x * math.cos(angle) - y * math.sin(angle), x * math.sin(angle) + y * math.cos(angle)
            floor.append([round(x + dx, 4), round(y + dy, 4), round(z, 4)])
        curves.append(floor)
    return {"system": SYSTEM, "source": "python", "curves": curves, "floor_height": p["floor_height"]}
