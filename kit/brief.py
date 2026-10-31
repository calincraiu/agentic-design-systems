"""Structured design briefs: load them and check them against kit/schemas/brief.schema.json.

The schema is generic. Each design system adds its own checks on top (for example,
that constraint metrics are ones its evaluator actually measures).
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).parent / "schemas" / "brief.schema.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def problems(brief):
    """Every way the brief breaks the schema, as readable sentences (empty list = valid)."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    found = []
    for error in sorted(Draft202012Validator(schema).iter_errors(brief), key=lambda e: list(e.path)):
        where = ".".join(str(p) for p in error.path) or "(top level)"
        found.append(f"{where}: {error.message}")
    return found
