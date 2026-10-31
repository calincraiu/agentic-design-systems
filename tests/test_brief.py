import copy

from examples.tower.cli import tower_problems
from kit import brief as briefs
from kit.paths import ROOT

REFERENCE = ROOT / "examples" / "tower" / "briefs" / "lighthouse-keeper.json"


def test_reference_brief_is_valid():
    assert tower_problems(briefs.load(REFERENCE)) == []


def test_schema_problems_are_readable():
    brief = briefs.load(REFERENCE)
    del brief["summary"]
    brief["site"]["plot_width_m"] = -3
    found = briefs.problems(brief)
    assert any("summary" in p for p in found)
    assert any(p.startswith("site.plot_width_m") for p in found)


def test_unknown_parameters_and_metrics_are_caught():
    brief = copy.deepcopy(briefs.load(REFERENCE))
    brief["qualities"][0]["parameters"].append("colour")
    brief["constraints"][0]["metric"] = "beauty"
    found = tower_problems(brief)
    assert any("colour" in p for p in found)
    assert any("beauty" in p for p in found)
