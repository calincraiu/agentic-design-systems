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


def test_every_widget_on_a_slide_is_one_the_app_knows():
    import re
    js = (main.ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    registry = re.search(r"const WIDGETS = \{(.*?)\};", js, re.S).group(1)
    known = set(re.findall(r'(?:^|,)\s*"?([\w-]+)"?', registry))  # the keys: each follows a comma
    for deck in main.decks():
        for s in main.deck_slides(deck):
            for name in re.findall(r'data-widget="([^"]+)"', s["text"]):
                assert name in known, (s["file"], name)


def test_add_widget_runs_the_real_tool_exactly(client):
    r = client.get("/api/add", params={"numbers": "8437209516384.27 6958173402659.86"}).json()
    assert r["code"] == 0 and r["total"] == "15395382919044.13"
    assert r["command"] == "uv run tools/add.py 8437209516384.27 6958173402659.86"
    assert client.get("/api/add", params={"numbers": "0.1 0.2"}).json()["total"] == "0.3"
    bad = client.get("/api/add", params={"numbers": "1,000 2"}).json()
    assert bad["code"] == 2 and bad["total"] is None


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
    assert "ask me where I unzipped the course folder" in k["prompt"]


def test_two_kits_share_one_prompt_and_one_zip(client):
    k = client.get("/api/kits/add,dice").json()
    assert str(main.KITS / "add") in k["prompt"] and str(main.KITS / "dice") in k["prompt"]
    assert "tools/add.py" in k["files"] and "tools/dice.py" in k["files"]
    assert k["files"].count(".claude/settings.json") == 1
    names = zipfile.ZipFile(io.BytesIO(client.get("/kits/add,dice.zip").content)).namelist()
    assert "tools/add.py" in names and "tools/dice.py" in names and names.count(".claude/settings.json") == 1
    assert client.get("/api/kits/add,nope").status_code == 404


# The look of the deck: layouts, notes, figures and the live preview ---------------------------------------


def test_slide_header_and_notes_are_split_out():
    s = main.split_slide("<!-- layout: task | where: code-yours | time: 25 min | pairs -->\n# Hi\n\nbody\n\n<!-- notes -->\nsay this\n")
    assert (s["layout"], s["where"], s["time"], s["pairs"]) == ("task", "code-yours", "25 min", True)
    assert s["body"] == "# Hi\n\nbody" and s["notes"] == "say this" and s["title"] == "Hi"
    plain = main.split_slide("# Plain\n\ntext")
    assert plain["layout"] == "stage" and plain["where"] is None and plain["notes"] == ""
    odd = main.split_slide("<!-- layout: spinning | where: the-moon -->\n# X")
    assert odd["layout"] == "stage" and odd["where"] is None


def test_every_slide_declares_a_known_layout_and_place():
    for s in main.deck_slides("session-1"):
        assert s["text"].lstrip().startswith("<!-- layout:"), s["file"]
        assert s["where"] in main.WHERE, s["file"]
        assert s["title"], s["file"]


def test_notes_are_hidden_on_the_slide(client):
    slides = main.deck_slides("session-1")
    n, s = next((i, s) for i, s in enumerate(slides, 1) if s["notes"])
    marker = main.render(s["notes"])[:60]
    before, aside, after = client.get(f"/d/session-1/{n}").text.partition('<aside id="notes" class="notes" hidden>')
    assert aside and marker in after and marker not in before  # only inside the hidden drawer


def test_slides_with_notes_show_a_notes_button_and_others_do_not(client):
    slides = main.deck_slides("session-1")
    outline = client.get("/api/deck/session-1").json()
    for i, s in enumerate(slides, 1):
        assert outline[i - 1]["notes"] == bool(s["notes"])
        assert ("data-notes" in client.get(f"/d/session-1/{i}").text) == bool(s["notes"]), s["file"]


def test_figures_and_images_the_slides_ask_for_exist():
    import re
    from xml.dom import minidom
    for deck in main.decks():
        for s in main.deck_slides(deck):
            for name in re.findall(r'data-name="([\w-]+)"', s["text"]):
                svg = main.SLIDES / "figures" / f"{name}.svg"
                assert svg.is_file(), (s["file"], name)
                minidom.parse(str(svg))
            for image in re.findall(r'data-images="([^"]+)"', s["text"]):
                for name in image.split(","):
                    assert (main.ROOT / "app" / "static" / "img" / f"{name.strip()}.png").is_file(), name


def test_figure_steps_are_whole_numbers_counting_up_from_one():
    import re
    for svg in (main.SLIDES / "figures").glob("*.svg"):
        steps = sorted({int(n) for n in re.findall(r'data-step="(\d+)"', svg.read_text(encoding="utf-8"))})
        assert steps == list(range(1, len(steps) + 1)) or not steps, svg.name


def test_deck_outline_lists_every_slide(client):
    outline = client.get("/api/deck/session-1").json()
    assert [o["n"] for o in outline] == list(range(1, len(main.deck_slides("session-1")) + 1))
    assert all(o["title"] for o in outline)
    assert client.get("/api/deck/nope").status_code == 404
    assert client.get("/api/figure/loop").status_code == 200 and client.get("/api/figure/..").status_code in (404, 422)


def test_live_preview_is_the_towers_own_geometry(client):
    params = {"floors": 12, "twist": 90, "taper": 0.7, "lean": 5, "lean_dir": 90}
    got = client.get("/api/tower/preview", params=params).json()
    want = tower.build(params)
    assert got["curves"] == [[[x, y] for x, y, _ in floor] for floor in want["curves"]]
    assert client.get("/api/tower/preview", params={"taper": 5}).status_code == 400
    assert client.get("/api/tower/preview", params={"floors": "abc"}).status_code == 400
    assert client.get("/api/tower/preview", params={"colour": 1}).status_code == 400


def test_lists_without_a_blank_line_still_render_as_lists(client):
    text = "**On the plot**\n- Plot: 12\n- Tall\n- Top"
    assert main.blank_line_before_lists(text) == "**On the plot**\n\n- Plot: 12\n- Tall\n- Top"
    html = client.get("/api/file", params={"path": "kits/tool-spec/tools/stair_check.md", "render_md": True}).json()["html"]
    assert "<li>" in html and "<p>" in html


def test_slides_never_name_a_path_on_one_particular_computer():
    import re
    for deck in main.decks():
        for s in main.deck_slides(deck):
            assert not re.search(r"[A-Za-z]:[\\/]|/Users/|/home/", s["text"]), s["file"]


def test_every_page_has_the_keys_button(client):
    for url in ("/", "/d/session-1/1", "/p/concepts"):
        assert "data-keys" in client.get(url).text, url


def test_section_slides_open_each_part_of_the_session(client):
    slides = main.deck_slides("session-1")
    sections = [(i, s) for i, s in enumerate(slides, 1) if s["layout"] == "section"]
    assert len(sections) >= 5 and all(s["title"] for _, s in sections)
    n = sections[0][0]
    assert 'class="slide layout-section"' in client.get(f"/d/session-1/{n}").text


def test_task_slides_show_time_and_pairs_badges_but_not_the_chip_twice(client):
    n = next(i for i, s in enumerate(main.deck_slides("session-1"), 1) if s["layout"] == "task" and s["pairs"])
    html = client.get(f"/d/session-1/{n}").text
    assert 'class="badge">in pairs' in html and html.count('class="chip where-') == 1   # only in the title block
    assert html.count("badge") >= 2

