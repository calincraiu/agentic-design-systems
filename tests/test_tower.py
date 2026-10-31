import math

import pytest

from examples.tower.evaluate import evaluate
from examples.tower.generate import build
from examples.tower.params import resolve
from kit import geometry as geo


def test_resolve_fills_defaults_and_rejects_bad_values():
    assert resolve({})["floors"] == 12
    with pytest.raises(ValueError) as e:
        resolve({"floors": 200, "twist": 9999, "colour": "red"})
    message = str(e.value)
    assert "floors=200" in message and "twist=9999" in message and "colour" in message
    with pytest.raises(ValueError):
        resolve({"floors": 2.5})


def test_build_stacks_floors():
    g = build({"floors": 10, "floor_height": 4})
    assert len(g["curves"]) == 10
    assert [f[0][2] for f in g["curves"]] == [i * 4 for i in range(10)]


def test_twist_rotates_the_top_floor():
    g = build({"floors": 5, "width": 20, "depth": 10, "twist": 90})
    top = g["curves"][-1]
    xs = [p[0] for p in top]
    assert math.isclose(max(xs) - min(xs), 10, abs_tol=1e-3)  # depth now runs east-west


def test_taper_and_lean_move_the_top_floor():
    g = build({"floors": 11, "width": 20, "depth": 20, "taper": 0.5, "lean": 10, "lean_dir": 90})
    top = g["curves"][-1]
    assert math.isclose(geo.area(top), 100, rel_tol=1e-6)
    assert math.isclose(sum(p[0] for p in top) / 4, 10, abs_tol=1e-3)  # moved 10 m east


def test_evaluate_plain_box():
    r = evaluate(build({"floors": 10, "floor_height": 3, "width": 20, "depth": 10}))
    m = r["metrics"]
    assert m["height_m"] == 30
    assert m["gfa_m2"] == 2000
    assert m["footprint_m2"] == m["top_floor_m2"] == 200
    assert m["envelope_m2"] == 60 * 30 + 200
    assert m["max_cantilever_m"] == 0
    assert m["slenderness"] == 3
    assert m["shadow_m2"] >= m["footprint_m2"]
    assert m["site_coverage"] is None


def test_evaluate_with_brief_checks_constraints_and_plot():
    brief = {
        "site": {"plot_width_m": 20, "plot_depth_m": 20},
        "constraints": [
            {"metric": "height_m", "op": "<=", "value": 30, "source": "card"},
            {"metric": "beyond_plot_m", "op": "<=", "value": 0, "source": "assumed"},
        ],
    }
    r = evaluate(build({"floors": 12, "floor_height": 3, "width": 20, "depth": 20, "lean": 5}), brief)
    m = r["metrics"]
    assert m["site_coverage"] == 1
    assert m["beyond_plot_m"] == pytest.approx(5, abs=1e-3)
    assert m["max_cantilever_m"] == pytest.approx(5, abs=1e-3)
    assert [c["pass"] for c in r["constraints"]] == [False, False]


def test_brief_priorities_decide_what_is_better():
    plain = evaluate(build({}))
    assert "slenderness" not in plain["better"]  # a design judgement, not the tool's
    brief = {"site": {"plot_width_m": 20, "plot_depth_m": 20}, "constraints": [],
             "priorities": [{"metric": "slenderness", "goal": "max"}, {"metric": "shadow_m2", "goal": "max"}]}
    r = evaluate(build({}), brief)
    assert r["better"]["slenderness"] == "higher"
    assert r["better"]["shadow_m2"] == "higher"  # the brief overrides the default
    assert r["priorities"] == ["slenderness", "shadow_m2"]
