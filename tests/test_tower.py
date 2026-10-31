import math

import drawing
import pytest
from tower import build, evaluate, parse_limit, parse_plot, resolve


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
    assert math.isclose(drawing.area(top), 100, rel_tol=1e-6)
    assert math.isclose(sum(p[0] for p in top) / 4, 10, abs_tol=1e-3)  # moved 10 m east


def test_same_parameters_give_identical_results():
    params = {"floors": 30, "twist": 77, "taper": 1.3, "lean": 8, "lean_dir": 200}
    assert evaluate(build(params)) == evaluate(build(params))


def test_evaluate_plain_box():
    m = evaluate(build({"floors": 10, "floor_height": 3, "width": 20, "depth": 10}))["metrics"]
    assert m["height_m"] == 30
    assert m["gfa_m2"] == 2000
    assert m["footprint_m2"] == m["top_floor_m2"] == 200
    assert m["max_cantilever_m"] == 0
    assert m["slenderness"] == 3
    assert m["shadow_m2"] >= m["footprint_m2"]
    assert m["beyond_plot_m"] is None


def test_evaluate_checks_limits_and_plot():
    limits = [parse_limit("height_m<=30"), parse_limit("beyond_plot_m<=0"), parse_limit("floors>=12")]
    r = evaluate(build({"floors": 12, "floor_height": 3, "width": 20, "depth": 20, "lean": 5}), (20, 20), limits)
    assert r["metrics"]["beyond_plot_m"] == pytest.approx(5, abs=1e-3)
    assert r["metrics"]["max_cantilever_m"] == pytest.approx(5, abs=1e-3)
    assert [c["pass"] for c in r["limits"]] == [False, False, True]


def test_parse_limit_and_plot():
    assert parse_limit(" height_m > 180 ") == {"metric": "height_m", "op": ">", "value": 180}
    assert parse_plot("30x40") == (30, 40)
    for bad in ("height_m=180", "beauty>5", "height_m>tall"):
        with pytest.raises(ValueError):
            parse_limit(bad)
    for bad in ("12", "0x10", "ax b"):
        with pytest.raises(ValueError):
            parse_plot(bad)
