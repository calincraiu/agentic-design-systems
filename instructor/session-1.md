# Session 1: instructor notes

**Aim.** Students can tell apart an LLM, a tool, an agent, a skill and context, because they have seen each one do something the others can't. By the end, they have **their own folder** with a `CLAUDE.md`, a dice skill they wrote, a design stance and (if time allows) a first tool contract. No Rhino in this session.

**Two folders, said early and often:** the course folder is run and read, never worked in. It's replaced each session. Their own folder is where all authorship happens.

## Run-sheet (3 h)

The slides are `slides/session-1/` in the course app (`uv run course`). They alternate between the app (concepts, widgets) and Claude's Code tab (demos and student work).

| Time | Slide | Activity | Where |
|---|---|---|---|
| 0:00–0:10 | 1 | Hook: a finished gallery. "How would you know if any of this is good?" | App (prepared runs) |
| 0:10–0:25 | 2 | Two folders. Anyone without the app: `/setup`, `/start` in the course folder | App + Code tab |
| 0:25–0:35 | 3 | LLM: number poll in Chat. Type the answers into the widget, then roll 200 real d20s | App |
| 0:35–0:45 | 4–5 | Tool: dice widget, read `dice.py`. Agent: "roll until a double" demo | App ↔ **your** folder |
| 0:45–0:55 | 6–7 | Skill anatomy; `/tie-breaker` demo. Context stepper; the commentator line demo | App ↔ your folder |
| 0:55–1:20 | 8–9 | Students start their own folder, write `CLAUDE.md`, take the dice kit, write their own skill | Their folder |
| 1:20–1:35 | | Break | |
| 1:35–1:55 | 10–11 | Tower explorer in the app; `/tower-designer` demo on The Needle | App ↔ your folder |
| 1:55–2:25 | 12 | Students take the tower kit and write a stance; run it on a card | Their folder |
| 2:25–2:50 | 13 | Own tool, spec first: fill in `TEMPLATE.md`, `/tool-builder` | Their folder |
| 2:50–3:00 | 14 | Crit: "What could your skill **not** change?" | |

**If you're behind:** move slide 13 (own tool) to the start of Session 2, where it leads into *Tool* and *Measure* on the ladder. Keep the stance: it's the authorship, and it sets up the crit.

## Your demo folder

Do the demos in **your own folder**, built with the same take-away kits the students use, not in the course repo. Students then see exactly what they'll do. Before class: make an empty folder, write a short `CLAUDE.md`, copy in the `dice` and `tower` kits, and run `/tower-designer` on The Needle so its `runs/` is ready.

For the hook slide, the app's gallery shows the course folder's `runs/`. Either build a few towers in the explorer beforehand, or copy your demo folder's `runs/` into the course folder's `runs/`.

## Teaching Part 1

| Step | Say | Watch for |
|---|---|---|
| Number poll | "Nothing was rolled." Type the class's numbers into the widget. | **Try it beforehand.** If Chat runs code to answer, or the answers don't cluster, ask instead: "How do you know that number was random?" |
| Tool | Read all of `dice.py` aloud. Open "Behind the scenes" on the widget: the same command the agent runs. | The fear of code is the thing to remove here. |
| Agent | "You didn't tell it how many times." | Claude may write a small loop instead of calling the tool repeatedly. That's still the agent deciding how, so point it out. |
| Skill | Click through the anatomy; then have someone ask for a re-roll, and ask which option Claude prefers. | The file is the point: it's only text. |
| Context | Step through the stepper to step 5: what survives a new session. Then the commentator demo. | Needs a **new session**. Delete the line afterwards. |
| Own skill | "What can your skill not make the tool do?" | The agent may simply *say* it rolled a 7. Good discussion: the tool can't, but the LLM can still write it. That's why "never make up a roll" belongs in their `CLAUDE.md`. |

## Teaching the own tool

The point is that **authoring a tool means authoring its contract**: inputs, ranges, the rule in words, the output, and test cases worked out by hand. Students don't need to read the code: `/tool-builder` writes it, then runs *their* test cases. Its most useful moment is step 2, when it questions the contract before writing anything: unclear rounding, a missing unit, a test case the rule doesn't produce. Ask: "When a test fails, who was wrong?"

Good sizes: stair fit (the worked example), brick coursing, ramp gradient, parking count, room-area schedule. Too big: anything needing geometry, images or the internet.

## The cards

What each card hides, the questions a good agent should ask, and what the tower **cannot** measure. That last column feeds the crit and Session 2.

| Card | Hidden contradiction | Good questions | What the tower can't measure |
|---|---|---|---|
| Lighthouse Keeper | Visible from far away vs afraid of heights | How high is the headland? Would the keeper live higher up? | Visibility range (the agent has to reason it out) |
| The Spreadsheet | Maximum area vs "look expensive" | What does expensive look like to you? Any shadow rules? | Appearance, cost |
| Quiet Landmark | Memorable vs "doesn't shout"; height vs the residents' sun to the north | How tall is memorable? Which afternoon (season, time)? | Memorability; shadow is for one fixed sun position |
| The Needle | 144 m² plot vs a >400 m² penthouse (taper ≥ 1.7, or lean); tallest vs slenderness | May it overhang the street? How much taller than 180 m? | Structure, air rights |
| The Poet | Turning its back vs "nothing dramatic" | How much turn is "slowly"? Which way should the top face? | Views and orientation |
| The Co-op | Near the garden (low) vs light (thin) vs fair (equal floors) | How many floors is "a few"? What does fair mean? | Daylight, fairness, distance to the garden |
| Climbing Gym | Overhangs vs stability and cost | How big is a "no way" overhang? Budget? | Cost, structural risk |
| Vertical School | 4,800 m² on a 35 × 35 m plot vs "never a skyscraper"; terraces need taper | What height feels like a skyscraper to a child? How much play area? | **Terrace area: no metric for it.** The perfect Session 2 seed |

Also expect this limit to come up on The Needle: taper is linear, so a tower can't "stay thin and flare near the top". That's another good Session 2 prompt.

## Likely problems

- **Students work in the course folder.** In the student copy, Claude is told not to edit there, and edits are denied. If someone is stuck, check which folder their Code tab has open.
- **The take-away prompt doesn't copy the hidden `.claude` folder.** Ask Claude to list `.claude/skills/` afterwards. Fallback: the "download the kit as a zip" link under each prompt.
- **A new skill doesn't show up.** Start a new session. If it still doesn't, check the folder is directly in `.claude/skills/<name>/` and the file is called `SKILL.md`.
- **Students can't find `.claude/`.** Dot-folders are hidden in Finder and some file windows. Use the app's file pane, or ask Claude to open or copy the file.
- **The course app stops.** Started with `/start`, it lives as long as that Claude session. Run `/start` again, or use the double-click launcher.
- **Synced folders (OneDrive, iCloud).** These usually work, but can be slow or lock files. Prefer a local folder.
- **Permission prompts.** Each kit's `.claude/settings.json` pre-approves `uv run tools/...`. Anything else prompts, and that's worth a sentence: *the agent asks before acting outside its lane*.
- **The agent skips the client questions.** It shouldn't, because the skill says stop. If it does, ask the room why that matters: the human checkpoint is part of the workflow's design.
- **Two skills with similar descriptions.** Call them explicitly (`/tower-good-neighbour`) rather than relying on the agent to pick one.
- **The gallery doesn't update.** It's rebuilt after each run, but the page needs a refresh.
- **The stance run is labelled `tower-designer` in the gallery.** The student forgot to change the name in the copied skill. The skill tells Claude to pass its own name.
