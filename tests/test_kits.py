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
    added = run(tmp_path, "tools/add.py", "12.4", "18.75", "9.3", "22.05")
    assert added.returncode == 0 and "Total: 62.50" in added.stdout
    tower = run(tmp_path, "tools/tower/tower.py", "--floors", "6", "--label", "kit test")
    assert tower.returncode == 0, tower.stderr
    assert (tmp_path / "runs" / "gallery.html").exists()
    assert "Gallery: runs/gallery.html" in tower.stdout


def test_kit_settings_are_identical_so_copying_a_second_kit_is_harmless():
    settings = {(k / ".claude" / "settings.json").read_text(encoding="utf-8") for k in KITS.iterdir()}
    assert len(settings) == 1


def test_every_tool_declares_its_dependencies_inline():
    for tool in KITS.glob("*/tools/**/*.py"):
        if tool.name in ("drawing.py", "gallery.py", "runner.py"):  # plumbing; runner.py runs inside Rhino
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


# Grasshopper tools ------------------------------------------------------------
# The runner itself only works inside Rhino; its checks and receipts are plain Python.


def gh_runner():
    import importlib.util
    spec = importlib.util.spec_from_file_location("runner", KITS / "gh" / "tools" / "grasshopper" / "runner.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_refuses_what_a_slider_would_silently_clamp_or_round():
    check = gh_runner().check_slider_value
    assert check("a", 12.5, 0, 1000, 2) is None
    assert check("a", 0.1, 0, 1000, 2) is None
    assert "outside 0 to 1" in check("a", 12.5, 0, 1, 3)
    assert "more than 2 decimal places" in check("a", 0.125, 0, 1000, 2)
    assert "whole number" in check("floors", 3.5, 1, 80, 0, "integer")
    assert "even" in check("n", 3, 0, 10, 0, "even")
    assert check("n", 3, 0, 10, 0, "odd") is None
    assert "must be a number" in check("a", "1,5", 0, 1000, 2)
    assert "must be a number" in check("a", True, 0, 1, 0)


def test_runner_finds_layers_the_student_folder_and_names_receipts(tmp_path):
    from datetime import datetime
    r = gh_runner()
    assert r.layer_ref("layer:Site::Park") == "Site::Park"
    assert r.layer_ref("Site::Park") is None and r.layer_ref(3) is None
    gh = tmp_path / "tools" / "sum" / "sum.gh"
    assert r.project_folder(gh) == tmp_path.resolve()
    now = datetime(2026, 11, 21, 9, 5, 7)
    first = r.receipt_path(tmp_path, "sum", "A: tall/thin", now)
    assert first.name == "2026-11-21_090507_sum_A-tall-thin.json"
    first.parent.mkdir()
    first.write_text("{}")
    assert r.receipt_path(tmp_path, "sum", "A: tall/thin", now).name.endswith("_2.json")
    assert r.plain("42.5") == 42.5 and r.plain("3") == 3 and r.plain("park") == "park"
    assert r.choose("city", "sydney", ["London", "Sydney"]) == (1, None)
    index, problem = r.choose("city", "Cluj", ["London", "Sydney"])
    assert index is None and "not one of its choices: London, Sydney" in problem
    assert r.number(12.0) == "12" and r.number(8479.117241) == "8479.12" and r.number(0.3) == "0.3"
    assert "in:park was given nothing" in r.plain_message("in:park", "Floating parameter in:park failed to collect data")
    assert r.plain_message("Avr", "Input parameter I failed to collect data") == "Avr: Input parameter I failed to collect data"


def test_runner_summary_reads_like_a_receipt():
    r = gh_runner()
    ok = {"tool": "sum", "file": "tools/sum/sum.gh", "units": "Meters", "receipt": "runs/x.json", "geometry": False,
          "inputs": {"a": {"value": 12.5, "given": True}, "b": {"value": 2, "given": False}},
          "outputs": {"sum": 14.5}, "warnings": [], "errors": []}
    text = r.summary(ok)
    assert "a = 12.5, b = 2 (default)" in text and "sum = 14.5" in text and "Receipt: runs/x.json" in text
    assert "Units" not in text
    refused = {"tool": "sum", "file": "tools/sum/sum.gh", "refused": ["a = 2000 is outside 0 to 1000"],
               "inputs_available": ["a", "b"]}
    assert "REFUSED" in r.summary(refused) and "Inputs it takes: a, b" in r.summary(refused)


def test_every_grasshopper_tool_has_a_contract_with_test_cases():
    tools = list(KITS.glob("*/tools/*/*.gh"))
    assert tools
    for gh in tools:
        contract = gh.with_suffix(".md")
        assert gh.parent.name == gh.stem, f"{gh}: a Grasshopper tool lives in tools/<name>/<name>.gh"
        assert contract.exists(), f"{gh} has no contract"
        text = contract.read_text(encoding="utf-8")
        assert "## Test cases" in text and "`in:" in text and "`out:" in text, contract


def test_the_grasshopper_tower_contract_matches_the_python_tower(tmp_path, monkeypatch):
    """tower.gh was checked against tower.py in Rhino with these cases; the contract must quote tower.py's numbers."""
    monkeypatch.delenv("ADS_RUNS_DIR", raising=False)
    contract = (KITS / "site" / "tools" / "tower" / "tower.md").read_text(encoding="utf-8")
    tool = KITS / "tower" / "tools" / "tower" / "tower.py"
    cases = [([], "4800", "42"),
             (["--floors", "30", "--floor-height", "3.2", "--width", "24", "--depth", "18", "--twist", "90",
               "--taper", "0.6", "--lean", "8", "--lean-dir", "45"], "8479.12", "96"),
             (["--floors", "1", "--width", "10", "--depth", "12"], "120", "3.5"),
             (["--floors", "40", "--width", "15.5", "--depth", "33.3", "--twist", "-200", "--taper", "1.8",
               "--lean", "40", "--lean-dir", "200"], "41623.7", "140")]
    for args, gfa, height in cases:
        out = run(tmp_path, str(tool), *args).stdout
        assert f"gfa_m2 = {gfa}" in out and f"height_m = {height} m" in out, (args, out)
        assert f"gfa_m2 = {gfa}" in contract and f"height_m = {height}`" in contract, args
    for args, beyond in (([], "0"), (cases[3][0], "55.52"), (["--floors", "30", "--lean", "20", "--lean-dir", "180"], "15"),
                         (["--width", "34"], "2")):
        out = run(tmp_path, str(tool), *args, "--plot", "30x30").stdout
        assert f"beyond_plot_m = {beyond}" in out and f"beyond_plot_m = {beyond}`" in contract, (args, out)


def test_every_measure_offers_a_row_for_the_tower_skill_that_names_a_real_tool():
    import re
    skill = (KITS / "site" / ".claude" / "skills" / "tower-in-rhino" / "SKILL.md").read_text(encoding="utf-8")
    assert "## Measures" in skill and "| Measure | Inputs | Limit |" in skill
    measures = list((KITS / "measures" / "tools").glob("*/*.md"))
    assert len(measures) >= 4
    for contract in measures:
        text = contract.read_text(encoding="utf-8")
        assert "## Use it in a skill" in text, contract
        row = re.search(r"`\| (tools/\S+\.gh) \|.*\| (\w+) *(<|>|<=|>=) *[\d.]+ \|`", text)
        assert row, f"{contract}: no row to paste into the Measures table"
        assert (KITS / "measures" / row[1]).exists(), row[1]
        assert f"`out:{row[2]}`" in text, f"{contract}: the limit names {row[2]}, which isn't an output"
