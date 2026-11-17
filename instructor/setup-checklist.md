# Setup checklists

## Students: before Session 1 (send a week ahead)

- [ ] Install the **Claude desktop app** and sign in with your course account.
- [ ] Unzip the course folder somewhere normal, such as `Documents/ads-course`. Avoid Downloads, and avoid OneDrive or iCloud folders if you can.
- [ ] In the app, go to the **Code** tab and choose that folder.
- [ ] Type `/setup-course` and let it run. Read each command before you approve it. Then type `/start-course`: the course app should open in your browser. If anything fails, bring the error message to the session.

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

- [ ] `/setup-course` installs uv and runs both tools. Does the app need a restart to find uv?
- [ ] `/start-course` opens the course app. Does it keep running while you carry on talking in the session?
- [ ] The double-click launchers: `Start course.cmd` on Windows (SmartScreen?), `Start course.command` on a Mac (right-click → Open the first time).
- [ ] In the course folder, ask Claude to "edit kits/dice/tools/dice.py". It should refuse and point you to your own folder, and the edit should be denied.
- [ ] Every slide's widgets load: add (calculator and the in-your-head poll), dice, the fairness poll, the `tries` tally (slide 21), tower explorer, skill anatomy, context stepper, take-away, gallery.
- [ ] The look, on the projector you'll use: the fonts load offline, the contrast is readable in light and dark (`D`), and nothing is cut off at the projector's resolution.
- [ ] Keys: `→`/`←` step through diagram parts, `N` opens notes, `G` shows all slides, `R` switches to reading mode and back, `?` (or the **Keys** button, top right) lists them all. The tower explorer's preview moves as you drag a slider.
- [ ] **Empty-folder walkthrough:** new folder → Code tab → write `CLAUDE.md` → copy in the add + dice kits by hand (slide 9: download the zip, unzip, drag `tools` and `.claude` across). Is the hidden `.claude` folder copied? Do `/add-up` and `/tie-breaker` appear in a new session?
- [ ] In that folder: "Roll two dice until you get a double" (slide 21), and the commentator line in `CLAUDE.md` (slide 29) in a new session.
- [ ] Permission prompts in the student's folder: `uv run tools/...` shouldn't prompt. On Windows without Git, check the PowerShell rules too.
- [ ] Tower kit: `/tower-designer` with a one-line wish (it should ask, then stop and wait), a stance skill, then `runs/gallery.html` in their folder. Does clicking it in a reply open the Browser pane, with images?
- [ ] Tool-spec kit (Session 2, but it ships in the zip): `/tool-builder` on `tools/stair_check.md`. It should build the tool and pass all four test cases.
- [ ] The tower wish (slide 3): paste it into a few fresh chats. Note what comes back: numbers, a name, any stated assumptions. You'll compare it with `/tower-designer` on slide 36.
- [ ] In-your-head poll (slide 13): ask Chat the long sum on the slide in a few fresh chats, then "How exactly did you work that out?". Does it get it right, or run code? If it is always right, use longer numbers or a column of 25 room areas.
- [ ] Fairness poll (slide 14): ask Chat the crit-order question in about ten fresh chats. Does it lean? If it barely does, add names or use a list in a meaningful order (most famous first).
- [ ] Add tool (slide 16): ask Chat "what is 1,5 + 2?" and note what it says.
- [ ] Optional, for the dice tool's notes (slide 18): ask Chat for 20 rolls of a die a few times and count back-to-back repeats (a fair die averages about 3). Note whether it runs code.
- [ ] `/course-tutor quiz me on session 1` asks sensible questions.

On your own machine, before releasing: `uv sync`, then `uv run pytest`.
