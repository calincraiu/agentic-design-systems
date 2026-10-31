"""The evaluator: measures a tower and checks it against a brief's constraints.

It only reads geometry (floor outlines + floor height), so it works the same
whether Grasshopper or Python generated the tower. Every number here is exact
geometry except shadow_m2, which is a deliberately rough proxy.
"""
import math
from dataclasses import dataclass

from kit import geometry as geo


@dataclass(frozen=True)
class Metric:
    label: str
    unit: str
    better: str | None  # default for the gallery; a brief's priorities override it. None = depends on the brief
    meaning: str


# Whether more or less is "better" is mostly a design judgement, so it belongs in the
# brief's priorities. Only near-universal defaults are set here.
METRICS = {
    "height_m": Metric("Height", "m", None, "Top of the roof above the ground."),
    "floors": Metric("Floors", "", None, "Number of storeys."),
    "gfa_m2": Metric("Floor area", "m2", None, "Gross floor area: all floor plates added up."),
    "footprint_m2": Metric("Footprint", "m2", None, "Area of the ground floor."),
    "top_floor_m2": Metric("Top floor", "m2", None, "Area of the highest floor plate."),
    "site_coverage": Metric("Site coverage", "", None, "Footprint divided by plot area (needs a brief)."),
    "beyond_plot_m": Metric("Beyond plot", "m", "lower", "How far any floor reaches past the plot boundary (needs a brief)."),
    "envelope_m2": Metric("Envelope", "m2", "lower", "Facade walls plus roof: a rough cost proxy."),
    "compactness": Metric("Compactness", "1/m", None, "Envelope area divided by volume. Low = compact (less heat loss); high = more facade per floor (more light)."),
    "slenderness": Metric("Slenderness", "", None, "Height divided by the narrowest side of the ground floor."),
    "max_cantilever_m": Metric("Max cantilever", "m", None, "Furthest any floor reaches beyond the ground floor footprint."),
    "shadow_m2": Metric("Shadow", "m2", "lower", "Ground area in shadow at the reference sun position (rough proxy)."),
}

DEFAULT_SUN = {"altitude_deg": 35, "azimuth_deg": 180}  # mid-afternoon-ish, sun in the south

OPS = {"<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b, "<": lambda a, b: a < b, ">": lambda a, b: a > b}


def shadow_polygon(curves, floor_height, sun):
    """Outline of the shadow on the ground: every corner projected away from the sun.

    It takes the convex hull of all projected corners, which overestimates the shadow
    of strongly twisted or leaning towers. Good enough to compare options, not to
    submit to a planning authority.
    """
    reach = 1 / math.tan(math.radians(sun["altitude_deg"]))
    az = math.radians(sun["azimuth_deg"])
    away = (-math.sin(az), -math.cos(az))  # shadows point away from the sun
    points = []
    for floor in curves:
        for x, y, z in floor:
            for h in (z, z + floor_height):
                points.append((x + away[0] * h * reach, y + away[1] * h * reach))
    return [list(p) for p in geo.convex_hull(points)]


def check(metrics, brief):
    """Compare metrics with the brief's hard constraints."""
    results = []
    for c in (brief or {}).get("constraints", []):
        actual = metrics.get(c["metric"])
        passed = None if actual is None else OPS[c["op"]](actual, c["value"])
        results.append({**c, "actual": actual, "pass": passed})
    return results


def evaluate(geometry, brief=None):
    curves = geometry["curves"]
    floor_height = float(geometry["floor_height"])
    if not curves:
        raise ValueError("The geometry has no floors in it.")
    plans = [[(p[0], p[1]) for p in floor] for floor in curves]
    areas = [geo.area(p) for p in plans]
    ground = plans[0]

    height = max(p[2] for floor in curves for p in floor) + floor_height
    volume = sum(areas) * floor_height
    envelope = sum(geo.perimeter(p) * floor_height for p in plans) + areas[-1]
    m = {
        "height_m": height,
        "floors": len(curves),
        "gfa_m2": sum(areas),
        "footprint_m2": areas[0],
        "top_floor_m2": areas[-1],
        "site_coverage": None,
        "beyond_plot_m": None,
        "envelope_m2": envelope,
        "compactness": envelope / volume,
        "slenderness": height / geo.shortest_edge(ground),
        "max_cantilever_m": max([geo.distance_outside(ground, v) for p in plans[1:] for v in p] or [0.0]),
    }

    site = (brief or {}).get("site", {})
    sun = site.get("sun", DEFAULT_SUN)
    shadow = shadow_polygon(curves, floor_height, sun)
    m["shadow_m2"] = geo.area(shadow)
    if site:
        plot = geo.rectangle(site["plot_width_m"], site["plot_depth_m"])
        m["site_coverage"] = areas[0] / geo.area(plot)
        m["beyond_plot_m"] = max(geo.distance_outside(plot, v) for p in plans for v in p)

    m = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m.items()}
    better = {k: v.better for k, v in METRICS.items() if v.better}
    for p in (brief or {}).get("priorities", []):
        better[p["metric"]] = "lower" if p["goal"] == "min" else "higher"
    return {
        "metrics": m,
        "labels": {k: v.label for k, v in METRICS.items()},
        "units": {k: v.unit for k, v in METRICS.items()},
        "better": better,
        "priorities": [p["metric"] for p in (brief or {}).get("priorities", [])],
        "constraints": check(m, brief),
        "sun": sun,
        "shadow": shadow,
    }
