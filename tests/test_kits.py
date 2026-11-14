"""The kits must work on their own, copied into an empty folder with no pyproject."""
import shutil
import subprocess
import sys
from pathlib import Path

KITS = Path(__file__).resolve().parents[1] / "kits"


def run(folder, *args):
    return subprocess.run([sys.executable, *args], cwd=folder, capture_output=True, text=True, encoding="utf-8")


def test_kits_work_in_an_empty_folder(tmp_path, monkeypatch):
    monkeypatch.delenv("ADS_RUNS_DIR")
    for kit in KITS.iterdir():
        shutil.copytree(kit, tmp_path, dirs_exist_ok=True)
    assert run(tmp_path, "tools/dice.py", "--count", "2").returncode == 0
    tower = run(tmp_path, "tools/tower/tower.py", "--floors", "6", "--label", "kit test")
    assert tower.returncode == 0, tower.stderr
    assert (tmp_path / "runs" / "gallery.html").exists()
    assert "Gallery: runs/gallery.html" in tower.stdout


def test_kit_settings_are_identical_so_copying_a_second_kit_is_harmless():
    settings = {(k / ".claude" / "settings.json").read_text(encoding="utf-8") for k in KITS.iterdir()}
    assert len(settings) == 1


def test_every_tool_declares_its_dependencies_inline():
    for tool in KITS.glob("*/tools/**/*.py"):
        if tool.name in ("drawing.py", "gallery.py"):
            continue
        assert tool.read_text(encoding="utf-8").startswith("# /// script"), tool


def test_stair_check_passes_the_test_cases_in_its_own_contract(tmp_path):
    tool = KITS / "tool-spec" / "tools" / "stair_check.py"
    first = run(tmp_path, str(tool), "--floor-height", "3", "--run", "4.5").stdout
    assert "Risers: 18 x 166.7 mm" in first and "Treads: 17 x 264.7 mm" in first and "FAIL  Blondel 598.0" in first
    second = run(tmp_path, str(tool), "--floor-height", "3", "--run", "4.8").stdout
    assert "FAIL" not in second and "Pitch: 30.6 deg" in second
    third = run(tmp_path, str(tool), "--floor-height", "2.8", "--run", "3").stdout
    assert "Risers: 16 x 175.0 mm" in third and "FAIL  going 200.0" in third and "FAIL  Blondel 550.0" in third
    assert run(tmp_path, str(tool), "--floor-height", "9", "--run", "4").returncode == 2
