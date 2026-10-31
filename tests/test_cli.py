import json

from examples.tower import cli as tower
from kit import cli as kit
from kit.paths import ROOT, exchange_dir, runs_dir

from .fake_gh import FakeGrasshopper

BRIEF = str(ROOT / "examples" / "tower" / "briefs" / "lighthouse-keeper.json")


def generate(capsys, *args):
    code = tower.main(["generate", *args])
    out = capsys.readouterr()
    return code, (json.loads(out.out) if code == 0 else None), out.err


def test_generate_with_python_backend_makes_a_complete_run(capsys):
    code, summary, _ = generate(capsys, "--backend", "python", "--floors", "8", "--floor-height", "3",
                                "--width", "16", "--depth", "16", "--brief", BRIEF, "--skill", "tower-designer", "--label", "A: squat", "--why", "grounded")
    assert code == 0
    run = runs_dir() / summary["run"].split("/")[-1]
    for name in ("meta.json", "brief.json", "params.json", "geometry.json", "metrics.json", "image.png"):
        assert (run / name).exists(), name
    assert summary["metrics"]["height_m"] == 24
    assert {c["metric"]: c["pass"] for c in summary["constraints"]} == {"beyond_plot_m": True, "height_m": True, "slenderness": True}
    gallery = (runs_dir() / "gallery.html").read_text(encoding="utf-8")
    assert "A: squat" in gallery and "The Lighthouse Keeper" in gallery


def test_generate_rejects_out_of_range_params(capsys):
    code, _, err = generate(capsys, "--backend", "python", "--taper", "5")
    assert code == 2 and "taper=5" in err
    assert not runs_dir().exists() or not any(runs_dir().iterdir())


def test_generate_through_the_bridge(capsys):
    exchange_dir().mkdir(parents=True)
    with FakeGrasshopper(exchange_dir()):
        code, summary, _ = generate(capsys, "--floors", "5", "--timeout", "5")
    assert code == 0
    assert summary["backend"] == "grasshopper" and summary["warnings"] == []


def test_failed_bridge_run_is_discarded(capsys):
    code, _, err = generate(capsys, "--timeout", "0.3")
    assert code == 2 and "did not answer" in err
    assert not [p for p in runs_dir().iterdir() if p.is_dir()]


def test_check_brief_and_params(capsys):
    assert tower.main(["check-brief", BRIEF]) == 0
    assert "Brief OK" in capsys.readouterr().out
    assert tower.main(["params"]) == 0
    assert "--lean-dir" in capsys.readouterr().out


def test_kit_ping_reports_missing_grasshopper(capsys):
    assert kit.main(["ping", "--timeout", "0.3"]) == 1
    assert "No answer" in capsys.readouterr().out
