# Session 1: instructor notes

**Aim.** Students can tell apart an LLM, a tool, an agent, a skill and context, because they have seen each one do something the others can't, and they have written two skills. No Rhino in this session.

## Run-sheet (3 h)

| Time | Activity | Material |
|---|---|---|
| 0:00–0:10 | Hook: show a finished gallery. Ask: "How would you know if any of this is good?" | Prepared `runs/` |
| 0:10–0:25 | `/setup` for anyone who hasn't done it | `README.md` |
| 0:25–1:10 | Part 1: LLM → tool → agent → skill → context → write a skill | `session-1/1-dice.md` |
| 1:10–1:25 | Break | |
| 1:25–2:20 | Part 2: meet the tower, take on a client, choose a direction | `session-1/2-tower.md` |
| 2:20–2:50 | Write a design stance, rerun, compare | `session-1/2-tower.md` |
| 2:50–3:00 | Crit: "What could your skill **not** change?" | |

**If you're behind:** cut the comparison between pairs in Part 2. Keep the stance, as it's the authorship and it sets up the crit.

## Preparing the hook

Run `/tower-designer` on The Needle before class, and keep the `runs/` folder. Its contradiction is easy to see: a 12 × 12 m plot against a penthouse over 400 m². Don't explain how the gallery was made. Part 2 gets back to it.

## Teaching Part 1

Do steps 1–5 together on the projector, about 5 minutes each, with students copying. Leave 15–20 minutes for step 6 in pairs.

| Step | Say | Watch for |
|---|---|---|
| 1. Number poll | "Nothing was rolled." Tally the answers on the board. | **Try it beforehand.** If Chat runs code to answer, or the answers don't cluster, ask instead: "How do you know that number was random?" |
| 2. Tool | Read all of `dice.py` aloud. | The fear of code is the thing to remove here. |
| 3. Agent | "You didn't tell it how many times." | Claude may write a small loop instead of calling the tool repeatedly. If it does, that's still the agent deciding how, so point it out. |
| 4. Skill | Have someone ask for a re-roll, then ask which option Claude prefers. | The file is the point: it's only text. |
| 5. Context | Show that neither the tool nor the skill changed. | Needs a **new session**. Make sure the line gets deleted afterwards. |
| 6. Own skill | "What can your skill not make the tool do?" | The agent may simply *say* it rolled a 7. Good discussion: the tool can't, but the LLM can still write it. That's why the rule "never make up a roll" is in `CLAUDE.md`. |

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

- **A new skill doesn't show up.** Start a new session. If it still doesn't, check the folder is directly in `.claude/skills/<name>/` and the file is called `SKILL.md`.
- **Students can't find `.claude/`.** Dot-folders are hidden in Finder and some file windows. Use the app's file pane, or ask Claude to open or copy the file.
- **Synced folders (OneDrive, iCloud).** These usually work, but can be slow or lock files. Prefer a local folder.
- **Permission prompts.** `.claude/settings.json` pre-approves the course tools and `uv sync`. Anything else prompts, and that's worth a sentence: *the agent asks before acting outside its lane*.
- **The agent skips the client questions.** It shouldn't, because the skill says stop. If it does, ask the room why that matters: the human checkpoint is part of the workflow's design.
- **Two skills with similar descriptions.** Call them explicitly (`/tower-good-neighbour`) rather than relying on the agent to pick one.
- **The gallery doesn't update.** It's rebuilt after each run, but the page needs a refresh.
- **The stance run is labelled `tower-designer` in the gallery.** The student forgot to change the name in the copied skill. The skill tells Claude to pass its own name.
