# Setup checklists

## Students: before Session 1 (send a week ahead)

- [ ] **Rhino 8** installed and licensed. Open Grasshopper once.
- [ ] **VS Code** installed.
- [ ] The **Claude Code** extension installed in VS Code, and signed in with your course account.
- [ ] The course repo downloaded and unzipped (or cloned) into a normal local folder, e.g. `Documents/ads-course`. Avoid Downloads, and avoid OneDrive or iCloud-synced folders if you can.
- [ ] Open that folder in VS Code and trust it when asked.
- [ ] Optional, and helpful: type `/setup` in the Claude Code panel and let it run. If anything fails, bring the error message to the session.

## Instructor: dry run before distributing

- [ ] `uv sync` and `uv run pytest`: all green.
- [ ] `examples/tower/tower.gh` built from [GH_SPEC.md](../examples/tower/GH_SPEC.md); its "Test it" steps pass in Rhino 7.
- [ ] `tower.gh` opened and tested (`kit ping`, `tower generate`) in **Rhino 8 on Windows** and **Rhino 8 on Mac**.
- [ ] A full student flow in VS Code with Claude Code: `/setup` → `/tower-designer` on two different cards → a stance skill from the template → gallery comparison.
- [ ] `/course-tutor quiz me on session 1` asks sensible questions.
- [ ] Delete `runs/`, `.exchange/` and anything in `studio/briefs/` before handing the repo out.
