# Setup checklists

## Students: before Session 1 (send a week ahead)

- [ ] Install the **Claude desktop app** and sign in with your course account.
- [ ] Unzip the course folder somewhere normal, such as `Documents/ads-course`. Avoid Downloads, and avoid OneDrive or iCloud folders if you can.
- [ ] In the app, go to the **Code** tab and choose that folder.
- [ ] Type `/setup` and let it run. Read each command before you approve it. If anything fails, bring the error message to the session.

Session 1 doesn't need Rhino.

## Instructor: make the student copy

Commit first: the zip contains only what's committed. From the repo folder:

```
git archive --format=zip -o ads-course.zip HEAD
```

`.gitattributes` leaves out `instructor/` and `tests/`. Your `runs/` isn't committed, so it isn't included either.

## Instructor: dry run before distributing

From the zip, on **Windows and a Mac**, in the desktop app's Code tab, ideally with no VS Code or Git installed:

- [ ] `/setup` installs uv and runs both tools. Does the app need a restart to find uv? (Students' `/setup` instructions cover this, but check.)
- [ ] `/tie-breaker` appears when you type `/`, and it runs.
- [ ] Permission prompts: `uv run tools/...` shouldn't prompt. On Windows without Git, commands go through PowerShell; check that its rules work too.
- [ ] Step 6: create a new skill. Does it appear in a new session? In the same session? Does writing to `.claude/skills/` prompt?
- [ ] Clicking `runs/gallery.html` in a reply opens the Browser pane, **with the images showing**. If it doesn't, use `uv run tools/gallery.py --open` in the material instead.
- [ ] Are tower images visible in the conversation or the file pane, or only in the gallery?
- [ ] Students can find and edit `.claude/skills/` and `CLAUDE.md` in the file pane.
- [ ] Number poll: ask Chat "Pick a random number from 1 to 20" several times, in fresh chats. Do the answers cluster? Does it run code?
- [ ] `/tower-designer` on two different cards, then a stance skill, then the gallery comparison.
- [ ] `/course-tutor quiz me on session 1` asks sensible questions.

On your own machine, before releasing: `uv sync`, then `uv run pytest`.
