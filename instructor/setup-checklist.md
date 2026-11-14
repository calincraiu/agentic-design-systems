# Setup checklists

## Students: before Session 1 (send a week ahead)

- [ ] Install the **Claude desktop app** and sign in with your course account.
- [ ] Unzip the course folder somewhere normal, such as `Documents/ads-course`. Avoid Downloads, and avoid OneDrive or iCloud folders if you can.
- [ ] In the app, go to the **Code** tab and choose that folder.
- [ ] Type `/setup` and let it run. Read each command before you approve it. Then type `/start`: the course app should open in your browser. If anything fails, bring the error message to the session.

Don't make your own folder yet: we do that together. Session 1 doesn't need Rhino.

## Instructor: make the student copy

Commit first: the zip contains only what's committed. Then:

```
uv run scripts/package.py
```

It writes `dist/ads-course.zip`. `.gitattributes` leaves out `instructor/`, `tests/`, `packaging/` and `scripts/`, and the files in `packaging/student/` replace `CLAUDE.md` and `.claude/settings.json` (no edits allowed in the course folder). Your `runs/` isn't committed, so it isn't included.

For later sessions, make a new zip. Students delete their old course folder and unzip the new one in its place. Their own folder isn't touched.

## Instructor: dry run before distributing

From the zip, on **Windows and a Mac**, in the desktop app's Code tab, ideally with no VS Code or Git installed:

- [ ] `/setup` installs uv and runs both tools. Does the app need a restart to find uv?
- [ ] `/start` opens the course app. Does it keep running while you carry on talking in the session?
- [ ] The double-click launchers: `Start course.cmd` on Windows (SmartScreen?), `Start course.command` on a Mac (right-click → Open the first time).
- [ ] In the course folder, ask Claude to "edit kits/dice/tools/dice.py". It should refuse and point you to your own folder, and the edit should be denied.
- [ ] Every slide's widgets load: dice, LLM vs tool, tower explorer, skill anatomy, context stepper, take-away, gallery.
- [ ] **Empty-folder walkthrough:** new folder → Code tab → write `CLAUDE.md` → paste the dice take-away prompt. Is the hidden `.claude` folder copied? Does `/tie-breaker` appear in a new session?
- [ ] Permission prompts in the student's folder: `uv run tools/...` shouldn't prompt. On Windows without Git, check the PowerShell rules too.
- [ ] Tower kit: `/tower-designer` on a card, a stance skill, then `runs/gallery.html` in their folder. Does clicking it in a reply open the Browser pane, with images?
- [ ] Tool-spec kit: `/tool-builder` on `tools/stair_check.md`. It should build the tool and pass all four test cases.
- [ ] Number poll: ask Chat "Pick a random number from 1 to 20" several times, in fresh chats. Do the answers cluster? Does it run code?
- [ ] `/course-tutor quiz me on session 1` asks sensible questions.

On your own machine, before releasing: `uv sync`, then `uv run pytest`.
