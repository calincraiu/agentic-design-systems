import subprocess
import sys
from pathlib import Path

import gallery
import tower

KITS = Path(__file__).resolve().parents[1] / "kits"


def dice(*args):
    script = KITS / "dice" / "tools" / "dice.py"
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


def test_dice_rolls_the_requested_dice_within_range():
    result = dice("--sides", "20", "--count", "50")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    rolls = [int(n) for n in lines[0].removeprefix("Rolls:").split()]
    assert len(rolls) == 50 and all(1 <= r <= 20 for r in rolls)
    assert lines[1] == f"Total: {sum(rolls)}"


def test_dice_rejects_impossible_requests():
    assert dice("--sides", "1").returncode == 2
    assert dice("--count", "0").returncode == 2


def test_tower_makes_a_complete_run(capsys):
    code = tower.main(["--floors", "8", "--floor-height", "3", "--width", "16", "--depth", "16", "--plot", "18x18",
                       "--require", "height_m<=30", "--require", "floors>10",
                       "--project", "The Keeper", "--skill", "tower-designer", "--label", "A: squat", "--why", "grounded"])
    out = capsys.readouterr().out
    assert code == 0
    assert "height_m = 24 m" in out and "beyond_plot_m = 0 m" in out
    assert "PASS  height_m <= 30" in out and "FAIL  floors > 10" in out
    run = next(p for p in gallery.runs_dir().iterdir() if p.is_dir())
    for name in ("run.json", "geometry.json", "image.png"):
        assert (run / name).exists(), name
    page = (gallery.runs_dir() / "gallery.html").read_text(encoding="utf-8")
    assert "A: squat" in page and "The Keeper" in page and "tower-designer" in page and 'class=fail' in page


def test_gallery_escapes_what_it_is_given(capsys):
    assert tower.main(["--label", "<b>bold</b>", "--why", "a & b"]) == 0
    page = (gallery.runs_dir() / "gallery.html").read_text(encoding="utf-8")
    assert "<b>bold</b>" not in page and "&lt;b&gt;" in page and "a &amp; b" in page


def test_bad_input_makes_no_run(capsys):
    assert tower.main(["--taper", "5"]) == 2
    assert "taper=5" in capsys.readouterr().err
    assert tower.main(["--require", "beauty>5"]) == 2
    assert tower.main(["--require", "beyond_plot_m<=0"]) == 2
    assert "needs a plot" in capsys.readouterr().err
    assert not gallery.runs_dir().exists() or not any(gallery.runs_dir().iterdir())
