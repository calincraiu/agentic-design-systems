# Agentic Design Systems: course repo (instructor copy)

This is the **instructor's** working copy of a 12-hour Masters module on agentic workflows for computational design. Students are architects, mostly not programmers. You're helping the instructor build and maintain the course.

Students never work in this repo. They get a zip of it (the "course folder"), made by `uv run scripts/package.py`. In that zip, `packaging/student/CLAUDE.md` and `packaging/student/.claude/settings.json` replace this file and the settings. The student versions tell Claude not to edit anything, and deny edits. Students build in **their own, separate folder**, starting empty, and copy in the kits.

## Repo map

| Path | What it is |
|---|---|
| `app/` | The course app (FastAPI). `main.py` serves slides and runs the kit tools; `static/app.js` holds the widgets |
| `slides/<deck>/NN-name.md` | One Markdown file per slide. Widgets are `<div data-widget="...">`. `{{COURSE_DIR}}` becomes the folder's full path |
| `slides/*.md` | Reference pages (for example `concepts.md`) |
| `kits/<name>/` | What students copy into their own folder, laid out as a project (`tools/`, `.claude/skills/`, ...). **The only copy of each tool**: the app runs these files directly |
| `.claude/skills/` | Course-folder skills: `setup`, `start`, `course-tutor` |
| `packaging/student/` | Files that replace their repo versions in the student zip |
| `scripts/package.py` | Builds `dist/ads-course.zip` |
| `instructor/` | Run-sheets and notes (left out of the zip) |
| `tests/` | `uv run pytest` (left out of the zip) |

## Rules for the kits

- Each tool must run in an **empty folder** with `uv run tools/...`: a `# /// script` header lists its dependencies, and output goes to the current folder (`runs/`).
- Each kit's `.claude/settings.json` must be **identical**, so copying a second kit is harmless. `tests/test_kits.py` checks this.
- `dice.py`, `tower.py` and `stair_check.py` are meant to be read by students. Keep them short and plain. `drawing.py` and `gallery.py` are plumbing.

## Tools and app

- `uv run course`: start the app (free port from 8765, opens the browser; `--no-browser`).
- `uv run pytest`: tests, including that every slide opens and that the kits work in an empty folder.
- Don't install other packages or tools without asking.

## Writing for students

Plain language, with architectural examples. Define technical terms the first time. When you write or change student-facing material, say in two or three sentences what it does and why.
