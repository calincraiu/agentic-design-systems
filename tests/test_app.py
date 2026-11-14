import io
import zipfile

import pytest
import tower
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "RUNS", tmp_path / "runs")
    return TestClient(main.app)


def test_every_slide_and_page_opens(client):
    assert client.get("/").status_code == 200
    for deck in main.decks():
        slides = main.deck_slides(deck)
        assert slides, deck
        for n in range(1, len(slides) + 1):
            assert client.get(f"/d/{deck}/{n}").status_code == 200, (deck, n)
        assert client.get(f"/d/{deck}/read").status_code == 200
        assert client.get(f"/d/{deck}/{len(slides) + 1}").status_code == 404
    assert client.get("/p/concepts").status_code == 200


def test_widgets_on_slides_point_at_real_files_and_kits(client):
    import re
    for deck in main.decks():
        for s in main.deck_slides(deck):
            for path in re.findall(r'data-path="([^"]+)"', s["text"]):
                assert client.get("/api/file", params={"path": path}).status_code == 200, (s["file"], path)
            for kit in re.findall(r'data-kit="([^"]+)"', s["text"]):
                assert client.get(f"/api/kits/{kit}").status_code == 200, (s["file"], kit)


def test_dice_widget_runs_the_real_tool(client):
    r = client.get("/api/dice", params={"sides": 20, "count": 30}).json()
    assert r["code"] == 0 and len(r["rolls"]) == 30 and all(1 <= n <= 20 for n in r["rolls"])
    assert r["command"] == "uv run tools/dice.py --sides 20 --count 30"
    assert client.get("/api/dice", params={"sides": 1}).json()["code"] == 2


def test_tower_widget_matches_the_tool(client):
    spec = client.get("/api/tower/spec").json()
    assert [p["name"] for p in spec["params"]] == [p.name for p in tower.PARAMS]
    assert [m["name"] for m in spec["metrics"]] == list(tower.METRICS)
    r = client.post("/api/tower", json={"params": {"floors": 10, "twist": 45}, "plot": "20x20",
                                        "require": ["height_m>30", ""], "label": "A: test"}).json()
    assert r["code"] == 0, r["stderr"]
    assert r["command"].startswith('uv run tools/tower/tower.py --floors 10 --twist 45 --plot 20x20 --require "height_m>30"')
    assert r["run"]["metrics"]["height_m"] == 35 and r["run"]["limits"][0]["pass"] is True
    assert (main.RUNS / r["image"].removeprefix("/runs/")).exists()
    bad = client.post("/api/tower", json={"params": {"taper": 5}}).json()
    assert bad["code"] == 2 and "taper" in bad["stderr"] and "run" not in bad


def test_files_outside_the_course_material_are_refused(client):
    assert client.get("/api/file", params={"path": "pyproject.toml"}).status_code == 404
    assert client.get("/api/file", params={"path": "../secret.txt"}).status_code == 404
    assert client.get("/api/kits/..").status_code == 404


def test_kit_zip_unpacks_into_a_project_layout(client):
    names = zipfile.ZipFile(io.BytesIO(client.get("/kits/dice.zip").content)).namelist()
    assert "tools/dice.py" in names and ".claude/skills/tie-breaker/SKILL.md" in names
    k = client.get("/api/kits/tower").json()
    assert "tools/tower/tower.py" in k["files"] and str(main.KITS / "tower") in k["prompt"]
