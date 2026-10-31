# Session 1: instructor notes

## Opening demo (20 min)

**Setup beforehand.** Rhino with `tower.gh` open (Agent control on). VS Code on the repo, with the Claude Code panel and a terminal. An empty `runs/`. Font size up.

1. Read **The Needle** card aloud. It is the most dramatic, and its contradiction (a 12 × 12 m plot against a penthouse over 400 m²) is easy to see.
2. `/tower-designer the needle`. While the agent works, open the brief it writes in `studio/briefs/` and point at one quality, its interpretation, and its parameters.
3. When it asks its questions, ask a student to play the billionaire. Their answers go into the brief.
4. Let the three variants build. Keep Rhino visible: the model jumping between variants is the moment.
5. Open the gallery and switch to Table view.
6. Close with: *"Everything you just saw is in files you can open. By 2:45 you'll have written the part that made the design decisions."*

**Fallback.** If the bridge fails live, say so. It's a good lesson about systems. Continue with `--backend python`.

## The cards

What each card hides, the questions a good agent should ask, and what the Tower Toy **cannot** measure. That last column feeds the mini-crit and Session 2.

| Card | Hidden contradiction | Good questions | What the tower can't measure |
|---|---|---|---|
| Lighthouse Keeper | Visible from far away vs afraid of heights | How high is the headland? Would the keeper live higher up? | Visibility range (the agent has to reason it out) |
| The Spreadsheet | Maximum area vs "look expensive" | What does expensive look like to you? Any shadow rules? | Appearance, cost |
| Quiet Landmark | Memorable vs "doesn't shout"; height vs the residents' sun to the north | How tall is memorable? Which afternoon (season, time)? | Memorability; the shadow is only for one sun position |
| The Needle | 144 m² plot vs a >400 m² penthouse (taper ≥ 1.7, or lean); tallest vs slenderness | May it overhang the street? How tall is the neighbour? | Structure, air rights |
| The Poet | Turning its back vs "nothing dramatic" | How much turn is "slowly"? Which way should the top face? | Views and orientation |
| The Co-op | Near the garden (low) vs light (thin, less compact) vs fair (equal floors) | How many floors is "a few"? What does fair mean? | Daylight, fairness, distance to the garden |
| Climbing Gym | Overhangs vs stability and cost | How big is a "no way" overhang? Budget? | Cost, structural risk |
| Vertical School | 4,800 m² on a 35 × 35 m plot vs "never a skyscraper"; terraces need taper | What height feels like a skyscraper to a child? How much play area? | **Terrace area: no metric for it.** The perfect Session 2 seed |

## Likely problems

- **The Listener says "save this definition inside the course repo".** The student opened `tower.gh` from somewhere else (e-mail, Downloads, a copy). Open it from the repo folder.
- **Synced folders (OneDrive, iCloud).** These usually work, but can be slow or lock files. Prefer a local folder.
- **Permission prompts.** `.claude/settings.json` pre-approves `uv run tower/kit` and `uv sync`. Anything else prompts, and that is worth a sentence: *the agent asks before acting outside its lane*.
- **The agent skips the client questions.** It shouldn't, because the skill says stop. If it does, ask the room why that matters: the human checkpoint is part of the workflow's design.
- **Two skills with similar descriptions.** Call them explicitly (`/tower-good-neighbour`) rather than relying on the agent to pick one.
- **The gallery doesn't update.** It is rebuilt after each run, but the browser needs a refresh.

## Maintenance

The stance template points to `tower-designer`'s workflow instead of copying it. If you change the workflow, every stance skill follows automatically.
