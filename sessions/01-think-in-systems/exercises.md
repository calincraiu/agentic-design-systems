# Session 1 exercises

Work in pairs. One laptop drives (VS Code + Claude Code); the other person keeps notes and, in E3, plays the client.

## E1 · Set up and make a first tower (25 min)

1. Open this repo folder in VS Code and open the Claude Code panel.
2. Type `/setup` and follow along. Read what each command does before you approve it.
3. When Rhino updates by itself, you've connected an agent to Grasshopper.

**You're done when** the gallery shows two "setup" towers: one from Python, one from Grasshopper.

## E2 · Map the system (30 min)

The Tower Toy is a small but complete agentic design system. Find its parts:

| Part | Find it | Write down |
|---|---|---|
| The agent | | What can it decide on its own? |
| The tools | `uv run tower --help`, `uv run tower params` | What goes in, what comes out? |
| The skill | `.claude/skills/tower-designer/` | Which part is workflow, which part is design stance? |
| The context | `CLAUDE.md`, a brief | What does the agent know before you ask anything? |
| The evaluator | `examples/tower/evaluate.py` | Which metric would you trust least? Why? |
| The bridge | `kit/gh/`, `examples/tower/tower.gh` | How does a number get from the agent into a Grasshopper slider? |

Then **draw the system** on one page: boxes for the parts, arrows for what flows between them (text, numbers, geometry, images). Mark where *you* make decisions.

Check yourself with the tutor: `/course-tutor quiz me on session 1`.

## E3 · Brief as data (40 min)

1. Draw a client card from `clients/` (two pairs get the same card).
2. Run `/tower-designer` on your card. Stop when the agent pauses at its questions (step 4).
3. **Read the structured brief** it wrote in `studio/briefs/`. For each quality: do you agree with the interpretation? Edit what you don't. It's your brief.
4. Your partner plays the client and answers the questions **in character**. Make something up if needed, but stay consistent.
5. Let the agent finish: three variants, a comparison and a recommendation. Choose one direction yourselves.
6. Find the other pair with the same card. Compare your briefs side by side. **Where did you interpret the same words differently, and how did that change the towers?**

## E4 · Write a design stance (35 min)

The tower-designer's stance is "Balanced". Yours won't be.

1. Pick a stance and give it a name. For example:
   - *Good Neighbour*: the city comes first
   - *Sculptor*: form and silhouette lead
   - *Spreadsheet*: efficiency, always
   - *Storyteller*: the client's words, taken literally
   - or invent your own
2. Copy `templates/stance-skill/` to `.claude/skills/tower-<your-stance>/` (or ask the agent to do it) and fill in the template. Write it yourselves; this is the authorship part.
3. Run your new skill on **the same card and brief** as in E3.
4. Open the gallery and switch to *Table* view: your stance against Balanced, on the same brief.

**You're done when** the gallery shows runs from both skills under the same brief.

## Mini-crit (15 min)

Each pair shows the gallery and answers two questions:
1. What did your stance change?
2. What could your stance **not** change, however you wrote it?

The second answer sets up Session 2.

## Checkpoint questions

- What is the difference between a tool and a skill? Give an example of each from this repo.
- Why does the tower-designer stop and ask questions before generating anything?
- The agent says a variant is "elegant and grounded". What would you check before believing it?
- In the brief, why does each constraint record a `source`?
- If the client wants "lots of terraces", which part of the system would have to change to measure that?
- What happens to the design if you change the skill, and what happens if you change the tool?
