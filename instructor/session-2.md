# Session 2: instructor notes

**Aim.** Students can turn a Grasshopper definition into a tool that Claude runs (named inputs, named outputs, a contract), chain tools through layers, and write a skill that runs their tools with limits they can defend. By the end, their own folder holds two tools they built (`sum`, `daylit`), the tower on the real site, and a `tower-check` skill that `tower-in-rhino` uses to judge its variants.

**The thread.** One chain, built link by link: each thing students make is used by the next step.

> site → tower (given) → park_sun (given) / daylit (theirs) → tower-check (theirs) → tower-in-rhino → they decide

Part 1 builds the smallest possible tool by hand, which also checks every student's setup. Part 2 uses the same runner at the scale of a building, and students build a measure. Part 3 is the skill that wires the measures together with their limits. The lens throughout is scale: a definition wires components; a skill wires tools, in words. The `chain` figure is the map (slides 10, 14, 18). Session 1's wish, *"a tower on a 30 × 30 m plot next to a park: calm, but noticed from the river"*, comes back on slide 11 and in the design run on slide 16.

**The slide notes are for students.** Everything meant only for you is below.

## Before the session

- [ ] Students received the **before Session 2** list in `setup-checklist.md` a week ahead: Rhino 8 or 9, RhinoAI's MCP connected to the desktop app, Ladybug (with the Rhino 9 fix). Ask them to run `/setup-course` in the new course folder: its Rhino step checks all three.
- [ ] **Your demo folder:** your Session 1 demo folder. Build `sum.gh` by hand from slide 7 and `daylit.gh` from slide 13's recipe, so you know where beginners get stuck. Fill in `tower-check` with `park_sun` and `daylit`, and run `/tower-in-rhino` once with the wish.
- [ ] The reference `daylit` (`instructor/solutions/daylit/`) on a USB stick or shared drive, for a pair that can't finish it. It is not in the course zip.
- [ ] Rhino open, Grasshopper started, the canvas zoomed so the back row can read component names.

## Run-sheet (about 4 h)

| Time | Slides | Activity | Where |
|---|---|---|---|
| 0:00–0:10 | 1–4 | Title; outline; **Part 1** section; `add.py` vs `sum.gh` | App |
| 0:10–0:20 | 5 | Connect Claude to Rhino, take the `gh` kit | Their folder + Rhino |
| 0:20–0:45 | 6–7 | Anatomy; **everyone builds `sum.gh`**, following you on the projector, and writes `sum.md` | Rhino + their folder |
| 0:45–1:00 | 8–9 | The runner; Claude runs their `sum`: a receipt and a refusal. **This is the setup check** | App ↔ their folder |
| 1:00–1:30 | 10–12 | **Part 2** section; the wish on the site; take `site` + `measures`, open the site, a tower, a refusal, then each student picks one of the four given measures and runs it | App ↔ their folder + Rhino |
| 1:30–2:10 | 13 | **Pairs build `daylit`**, contract first | Rhino + their folder |
| 2:10–2:25 | | Break | |
| 2:25–2:35 | 14 | **Part 3** section: a skill wires tools; the context window | App |
| 2:35–3:10 | 15 | **Pairs write `tower-check`** and run it on their tower | Their folder |
| 3:10–3:35 | 16 | Paste the stance, `/tower-in-rhino` with the wish | Their folder + Rhino |
| 3:35–3:55 | 17 | Crit | App + their folders |
| 3:55–4:05 | 18–19 | The chain and the take-home; end | App |

**If you're behind:** build `daylit` together on the projector (slide 13) instead of in pairs, and do slide 16 as a demo in your folder with one pair's `tower-check` copied in. Keep `sum` (7–9: it's the setup check) and `tower-check` (15: it's the authorship).

## Slide by slide

| # | Slide | Do / say | Watch for |
|---|---|---|---|
| 4 | Same shape | Read the table row by row. Land on "what it accepts": the limit moves from code into the slider. | |
| 5 | Connect Rhino | Everyone asks "What's open in Rhino right now?" in a **new session** in their own folder. Walk the room: the reply must show a Rhino tool call. | No Rhino tools: MCP not connected (setup checklist). Claude starts a second Rhino: fine, use that one. The take-away copy prompt leaves their old `settings.json` alone: expected. |
| 6 | Anatomy | Press `→` four times. | |
| 7 | Build sum | Build it live, one step at a time, and wait for the room after each: place, wire, Edit… the sliders, rename, save. Show where the nickname field is in the right-click menu. | Nicknames without `in:`/`out:`. Saving outside their folder, or not in `tools/sum/`. Sliders left at the default range or as whole numbers. Claude offering to build the definition: stop it. |
| 8 | Runner | Press `→` five times. Stop on step 3: "the runner refuses what a slider would silently clamp". Show the three lines in the notes on the projector. | |
| 9 | Run sum | Everyone: 12.5 + 30, read the permission prompt, open the receipt, then 2000 + 1. Ask: where does 1000 come from? (Their slider.) **Anyone whose run fails has a setup problem: sort it out now, while the tool is trivial.** | Claude improvises a canvas-searching script instead of the three lines: deny it and point at the skill. First run slow (Grasshopper loading). If their own `sum.gh` is the problem and time is short, the `sum` kit (in the slide's drop-down) is a finished copy. |
| 10 | Part 2 | Press `→` to show the chain so far (site, tower, park_sun). "One tool's output is the next tool's input." | |
| 11 | The wish | Press `→` four times: plot, park, river and viewpoints, neighbours. "Last time the tool didn't know where the park was. Now it does." | |
| 12 | Tower + park_sun | Everyone opens the site (**Open**, not Import), asks for a tower in plain words, then 100 floors, then picks a measure and reads its contract before running it. Ask someone to read out the layer name Claude gave the measure. Point out that their next task is to build one of these. | Imported into a mm file: the runner warns about units. Students looking for old towers: layers under `runs::tower`. |
| 13 | daylit | Pairs, 40 min. They use the contract of the measure from slide 12 as the model. Insist on contract first: three test cases on paper before Grasshopper. Show once on the projector: the Curve parameter, Offset Curve with Negative, Flatten on Mass Addition's input, the Expression. At 30 min, show the 12 × 12 m test case on yours. | Positive offset distance (the core comes out bigger than the floor: daylit is negative). No Flatten: `dark_m2` shows one number per floor. No 0 merged in: the slim-tower case returns nothing. Claude treating "Curve offset failed" as a broken tool: the contract should say it's expected. |
| 14 | Part 3 | Press `→` to show `tower-check` around the measures. One minute on the context window: "New task, new session. What must last goes in a file." | |
| 15 | tower-check | Pairs, 35 min. Check each pair wrote a sentence for every limit before running. | Limits copied unchanged from the contracts: ask why that number. Rows pasted below the table instead of replacing *(none yet)*. Claude adding a measure or loosening a limit itself: the skill forbids it, so point at the rule. |
| 16 | Design with it | Everyone pastes their stance and runs the wish. Read one report's "judged by eye" line aloud. | Stance not pasted: the report says *Balanced*. `tower-in-rhino` measuring by itself instead of using `tower-check`: ask it to use the skill. Nothing passes: say it's a finding, not a bug. |
| 17 | Crit | Two or three pairs, both questions. Push on the second: every answer is a new tool or a judgement that stays human. | |
| 18 | The chain | The whole map. Point at the two links that are theirs. Take-home: the contract of a tool from their studio project. | |

## What to expect

Measured with the kits and the reference `daylit` (Rhino 9, London, the site as built):

- **`park_sun`:** a 12-floor 20 × 20 m tower takes 12.6% of the park's sun, a 40-floor one 18.8%. Above about 20 floors height barely matters (the 21 March shadow already reaches past the park); the footprint does: 21 × 21 m is 19.75%, 22 × 22 m 20.7%.
- **`daylit` (depth 7 m):** 20 × 20 m 91% (a 6 × 6 m core per floor, whatever the height or twist), 30 × 30 m 71.56%, 12 × 12 m 100% (with "Curve offset failed"), 30 floors tapering to half size 96.76%. Depth 5 m on 20 × 20 m: 75%.
- **The two pull the same way for once:** a slim footprint is kind to the park and daylit. What a slim tower trades away is floor area, which only shows up if a pair adds a floor-area wish or limit. If a pair asks why everything passes, that's a good crit question: what would a limit on floor area do?
- `daylit_percent >= 85` (the starting row in the reference contract) passes anything up to about 23 × 23 m.

## Likely problems

- **No Rhino tools in Claude.** The MCP server isn't connected to the desktop app (setup checklist). Not fixable in class in a minute: pair them with a neighbour. Slide 9 is where this shows up.
- **"No module named ladybug…"** on Rhino 9: the Ladybug installer gap (setup checklist). Pair them up for `park_sun`.
- **Units warning.** The site was imported into a millimetre file. Close it and File › Open `site/site.3dm`.
- **Two Rhinos.** The MCP started its own. Use that one, or close both and let it start one.
- **A measure gives 100% sun lost, or empty outputs, with "was given nothing".** An input wasn't given (usually the tower layer name is wrong). The layer is `runs::tower::<label as the runner wrote it>::mass`, e.g. `A-quiet-slab`.
- **Permission prompts on every run.** `run_python` asks each time by design. Students may choose "allow for this session" during Part 3; say what that means (any script, not only the runner).
