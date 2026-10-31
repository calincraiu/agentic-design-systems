"""A tool: builds a tower from eight numbers, measures it and saves the result.

Read it in three parts:
  1. PARAMETERS: everything the tool can be asked to do
  2. GENERATOR:  numbers in, floor outlines out
  3. MEASURES:   floor outlines in, metrics out

The agent can only express a design through these parameters, and can only judge
it through these metrics. Changing what is *possible* means changing this file,
not a skill.
"""
import argparse
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime

import drawing
import gallery

# 1. PARAMETERS ---------------------------------------------------------------


@dataclass(frozen=True)
class Param:
    name: str
    kind: type
    low: float
    high: float
    default: float
    unit: str
    meaning: str


PARAMS = [
    Param("floors", int, 1, 80, 12, "", "Number of storeys."),
    Param("floor_height", float, 2.8, 6.0, 3.5, "m", "Floor-to-floor height."),
    Param("width", float, 6, 60, 20, "m", "Ground floor size east-west."),
    Param("depth", float, 6, 60, 20, "m", "Ground floor size north-south."),
    Param("twist", float, -360, 360, 0, "deg", "Total rotation from the ground floor to the top floor (positive = anticlockwise from above)."),
    Param("taper", float, 0.2, 2.0, 1.0, "x", "Size of the top floor relative to the ground floor (below 1 narrows, above 1 widens)."),
    Param("lean", float, 0, 40, 0, "m", "How far the top floor is shifted sideways relative to the ground floor."),
    Param("lean_dir", float, 0, 360, 0, "deg", "Compass direction of the lean (0 = north, 90 = east, 180 = south)."),
]

BY_NAME = {p.name: p for p in PARAMS}


def resolve(given):
    """Fill in defaults and check every value. Raises ValueError listing all problems."""
    problems = [f"'{name}' is not a tower parameter" for name in sorted(set(given) - set(BY_NAME))]
    values = {}
    for p in PARAMS:
        value = given.get(p.name)
        if value is None:
            value = p.default
        if p.kind is int and float(value) != int(float(value)):
            problems.append(f"{p.name} must be a whole number (got {value})")
        value = p.kind(float(value)) if p.kind is int else float(value)
        if not p.low <= value <= p.high:
            problems.append(f"{p.name}={value:g} is outside {p.low:g} to {p.high:g} {p.unit}".rstrip())
        values[p.name] = value
    if problems:
        raise ValueError("; ".join(problems))
    return values


# 2. GENERATOR ----------------------------------------------------------------


def build(params):
    """Build the floor outlines.

    For each floor i, with t = i / (floors - 1) running from 0 (ground) to 1 (top):
      1. start from a width x depth rectangle centred on the origin
      2. scale it by 1 + (taper - 1) * t
      3. rotate it by twist * t degrees
      4. move it by lean * t towards lean_dir, and up to z = i * floor_height
    """
    p = resolve(params)
    n = p["floors"]
    base = drawing.rectangle(p["width"], p["depth"])
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
    return {"system": "tower", "source": "python", "curves": curves, "floor_height": p["floor_height"]}


# 3. MEASURES -----------------------------------------------------------------


@dataclass(frozen=True)
class Metric:
    label: str
    unit: str
    meaning: str


METRICS = {
    "height_m": Metric("Height", "m", "Top of the roof above the ground."),
    "floors": Metric("Floors", "", "Number of storeys."),
    "gfa_m2": Metric("Floor area", "m2", "Gross floor area: all floor plates added up."),
    "footprint_m2": Metric("Footprint", "m2", "Area of the ground floor."),
    "top_floor_m2": Metric("Top floor", "m2", "Area of the highest floor plate."),
    "beyond_plot_m": Metric("Beyond plot", "m", "How far any floor reaches past the plot boundary (needs --plot)."),
    "slenderness": Metric("Slenderness", "", "Height divided by the narrowest side of the ground floor."),
    "max_cantilever_m": Metric("Max cantilever", "m", "Furthest any floor reaches beyond the ground floor footprint."),
    "shadow_m2": Metric("Shadow", "m2", "Ground area in shadow with the sun in the south, 35 degrees up (a rough proxy)."),
}

SUN_ALTITUDE_DEG = 35
OPS = {"<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b, "<": lambda a, b: a < b, ">": lambda a, b: a > b}


def shadow_polygon(curves, floor_height):
    """Outline of the shadow on the ground: every corner projected north, away from the sun.

    It takes the convex hull of all projected corners, which overestimates the shadow
    of strongly twisted or leaning towers. Good enough to compare options, not to
    submit to a planning authority.
    """
    reach = 1 / math.tan(math.radians(SUN_ALTITUDE_DEG))
    points = []
    for floor in curves:
        for x, y, z in floor:
            points += [(x, y + z * reach), (x, y + (z + floor_height) * reach)]
    return [list(p) for p in drawing.convex_hull(points)]


def parse_limit(text):
    """Turn 'height_m>180' into its parts. Raises ValueError if it can't be read."""
    match = re.fullmatch(r"\s*(\w+)\s*(<=|>=|<|>)\s*(-?[\d.]+)\s*", text)
    if not match:
        raise ValueError(f"could not read the limit '{text}'; write it like \"height_m>180\"")
    metric, op, value = match.groups()
    if metric not in METRICS:
        raise ValueError(f"'{metric}' is not a metric; see --help for the list")
    return {"metric": metric, "op": op, "value": float(value)}


def parse_plot(text):
    """Turn '12x12' into (12.0, 12.0). Raises ValueError if it can't be read."""
    match = re.fullmatch(r"\s*([\d.]+)\s*[xX]\s*([\d.]+)\s*", text)
    if not match or float(match[1]) <= 0 or float(match[2]) <= 0:
        raise ValueError(f"could not read the plot '{text}'; write it like 12x12 (east-west x north-south, in metres)")
    return float(match[1]), float(match[2])


def evaluate(geometry, plot=None, limits=()):
    """Measure a tower from its floor outlines, and check it against any limits."""
    curves = geometry["curves"]
    floor_height = float(geometry["floor_height"])
    plans = [[(p[0], p[1]) for p in floor] for floor in curves]
    areas = [drawing.area(p) for p in plans]
    ground = plans[0]
    height = max(p[2] for floor in curves for p in floor) + floor_height
    shadow = shadow_polygon(curves, floor_height)

    m = {
        "height_m": height,
        "floors": len(curves),
        "gfa_m2": sum(areas),
        "footprint_m2": areas[0],
        "top_floor_m2": areas[-1],
        "beyond_plot_m": None,
        "slenderness": height / drawing.shortest_edge(ground),
        "max_cantilever_m": max([drawing.distance_outside(ground, v) for p in plans[1:] for v in p] or [0.0]),
        "shadow_m2": drawing.area(shadow),
    }
    if plot:
        boundary = drawing.rectangle(*plot)
        m["beyond_plot_m"] = max(drawing.distance_outside(boundary, v) for p in plans for v in p)
    m = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m.items()}

    checks = []
    for limit in limits:
        actual = m[limit["metric"]]
        checks.append({**limit, "actual": actual, "pass": None if actual is None else OPS[limit["op"]](actual, limit["value"])})
    return {"metrics": m, "limits": checks, "shadow": shadow}


# THE COMMAND -----------------------------------------------------------------


def generate(args):
    given = {p.name: getattr(args, p.name) for p in PARAMS if getattr(args, p.name) is not None}
    try:
        params = resolve(given)
        plot = parse_plot(args.plot) if args.plot else None
        limits = [parse_limit(text) for text in args.require]
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not plot and any(limit["metric"] == "beyond_plot_m" for limit in limits):
        print("ERROR: beyond_plot_m needs a plot: add --plot, like --plot 12x12", file=sys.stderr)
        return 2

    label = args.label or f"{params['floors']} floors, twist {params['twist']:g}"
    geometry = build(params)
    result = evaluate(geometry, plot, limits)
    m = result["metrics"]

    run = gallery.new_run(label)
    drawing.render_floors(geometry["curves"], geometry["floor_height"], run / "image.png", plot=plot, shadow=result["shadow"],
                          caption=f"{label}\nH {m['height_m']:g} m  |  GFA {m['gfa_m2']:,.0f} m2")
    gallery.write_json(run / "geometry.json", geometry)
    gallery.write_json(run / "run.json", {
        "label": label,
        "project": args.project,
        "skill": args.skill,
        "why": args.why or "",
        "created": datetime.now().isoformat(timespec="seconds"),
        "plot": plot,
        "params": params,
        "metrics": m,
        "limits": result["limits"],
        "headings": {k: f"{v.label} ({v.unit})" if v.unit else v.label for k, v in METRICS.items()},
    })
    page = gallery.build()

    print(f"Built: {label}")
    print("Parameters: " + ", ".join(f"{k}={v:g}" for k, v in params.items()))
    unset = [p.name for p in PARAMS if p.name not in given]
    if unset:
        print("Left at their defaults: " + ", ".join(unset))
    print("Metrics:")
    for name, value in m.items():
        if value is not None:
            print(f"  {name} = {value:g} {METRICS[name].unit}".rstrip())
    if result["limits"]:
        print("Limits:")
        for c in result["limits"]:
            print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['metric']} {c['op']} {c['value']:g}  (actual {c['actual']:g})")
    print(f"Image: {gallery.rel(run / 'image.png')}")
    print(f"Gallery: {gallery.rel(page)}")
    return 0


def main(argv=None):
    metrics = "\n".join(f"  {name:<17} {m.unit:<3} {m.meaning}" for name, m in METRICS.items())
    parser = argparse.ArgumentParser(
        description="Build one tower, measure it and save it as a run in runs/. Parameters left out use their defaults.",
        epilog=f"metrics (what the tool can measure, and what --require can check):\n{metrics}",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    for p in PARAMS:
        parser.add_argument("--" + p.name.replace("_", "-"), dest=p.name, type=p.kind, metavar=p.unit.upper() or "N",
                            help=f"{p.meaning} {p.low:g} to {p.high:g}, default {p.default:g}.")
    parser.add_argument("--plot", help="Size of the plot in metres, east-west x north-south, e.g. 12x12.")
    parser.add_argument("--require", action="append", default=[], metavar="LIMIT",
                        help="A hard limit to check, in quotes, e.g. \"height_m>180\". Repeat it for several limits.")
    parser.add_argument("--project", help="Name of the project (the client), so the gallery groups its runs together.")
    parser.add_argument("--skill", default="manual", help="Name of the skill producing this run (default: manual).")
    parser.add_argument("--label", help="Short name for this variant, e.g. 'A: slim beacon'.")
    parser.add_argument("--why", help="One or two sentences on the design intent of this variant.")
    return generate(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
