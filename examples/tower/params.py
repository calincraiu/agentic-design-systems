"""The tower's parameters: the contract between the agent and the generator.

Whatever the agent decides, it can only express it through these eight numbers,
within these ranges. Changing what is *possible* means changing this file and
the generators, not the skill.
"""
from dataclasses import dataclass


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
