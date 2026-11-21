# Session 2: instructor notes

**Aim.** Students can turn a Grasshopper definition into a tool that Claude runs (named inputs, named outputs, a contract), and can say what a measure does and doesn't see. By the end, their own folder has a Grasshopper tool they built (`floor_area`), the tower running on the real site, and a `tower-in-rhino` skill with two measures and limits they chose and can justify.

**The thread.** Session 1's wish, *"a tower on a 30 × 30 m plot next to a park: calm, but noticed from the river"*, now on a real site. Part 1 puts the tower there. Part 2 measures it, lets the room optimise one number, and then asks what the winner traded away.

**The slide notes are for students.** Everything meant only for you is below.

## Before the session

- [ ] Students received the **before Session 2** list in `setup-checklist.md` a week ahead: Rhino 8 or 9, RhinoAI's MCP connected to the desktop app, Ladybug (with the Rhino 9 fix). Ask them to run `/setup-course` in the new course folder: its Rhino step checks all three.
- [ ] **Your demo folder:** your Session 1 demo folder, plus the `gh`, `site` and `measures` kits. Build `floor_area.gh` yourself once (slide 11) so you know where beginners get stuck. Run `/tower-in-rhino` once with the wish, and once with the `park_sun` row and the challenge rules, so you know what to expect (see "What to expect in the challenge": height is free, and the winner is likely a 280 m tower widening upward).
- [ ] Rhino open with `site/site.3dm` from your demo folder (**File › Open**, not Import).
- [ ] Clear the scoreboard on slide 16 if you rehearsed with it (it remembers entries in the browser).

## Run-sheet (about 4 h)

| Time | Slides | Activity | Where |
|---|---|---|---|
| 0:00–0:15 | 1–5 | Title; outline; the wish on the site plan; the room calls out their take-home; the context window | App |
| 0:15–0:35 | 6–9 | **Part 1 · Tool.** Connect Claude to Rhino, take the `gh` kit; the runner diagram; everyone runs `sum.gh`, reads a receipt, gets a refusal | App ↔ their folder + Rhino |
| 0:35–1:10 | 10–11 | Anatomy of a Grasshopper tool; **pairs build `floor_area.gh`** and its contract | Rhino + their folder |
| 1:10–1:40 | 12 | Take the `site` kit, open the site, paste the stance, `/tower-in-rhino` with the wish | Their folder + Rhino |
| 1:40–1:55 | | Break | |
| 1:55–2:05 | 13–14 | **Part 2 · Measure.** Take the `measures` kit, paste the `park_sun` row | Their folder |
| 2:05–2:35 | 15–16 | **The challenge**, pairs, 25 min; scoreboard | Their folder ↔ App |
| 2:35–2:50 | 17 | Look at the winner: Goodhart | App |
| 2:50–3:30 | 18–19 | The menu; **choose what counts**, pairs, 35 min | App ↔ their folder |
| 3:30–3:50 | 20 | Crit | App + their folders |
| 3:50–4:05 | 21–22 | Ladder and take-home; end | App |

**If you're behind:** cut slide 13's demo to one sentence, and shorten *Choose what counts* to one measure chosen by the whole room (put its row on the projector). Keep `floor_area` (slide 11), the challenge (15–16) and the winner (17): they are the session.

## Slide by slide

| # | Slide | Do / say | Watch for |
|---|---|---|---|
| 3 | The wish | Press `→` four times: plot, park, river and viewpoints, neighbours. "Last time the tool didn't know where the park was. Now it does." | |
| 4 | What no metric captured | Collect answers out loud, write them up. Group them: sun/shadow, view, outdoor space, neighbours, "can't be measured". Point at the groups again on slide 18. | Nobody did the homework: ask what they *wanted* the tower to do that no slider could. |
| 5 | Context window | One minute. "New task, new session" is the habit; files are the memory. | |
| 7 | Connect Rhino | Everyone asks "What's open in Rhino right now?" in a **new session** in their own folder. Walk the room: the reply must show a Rhino tool call. | No Rhino tools: MCP not connected (setup checklist). Claude starts a second Rhino: fine, use that one. The take-away copy prompt leaves their old `settings.json` alone: expected. |
| 8 | Runner | Press `→` five times. Stop on step 3: "the runner refuses what a slider would silently clamp". Show the three lines in the notes on the projector. | |
| 9 | Run sum | Everyone: 12.5 + 30, read the permission prompt, open the receipt, then 2000 + 1. Ask: where does 1000 come from? (The slider.) | Claude improvises a canvas-searching script instead of the three lines: deny it and point at the skill. First run slow (Grasshopper loading). |
| 11 | floor_area | Pairs, 30 min. Insist on contract first: ranges and two test cases on paper before Grasshopper. Show once on the projector: place a slider, Edit… its range, rename it `in:width`. | Nicknames without `in:`/`out:` ("no inputs" / "no outputs"). Saving outside their folder, or not in `tools/floor_area/`. Floors slider left as a float. Claude offering to build the definition: stop it. |
| 12 | Tower in Rhino | Everyone opens the site (**Open**, not Import), pastes their stance, runs the wish. Read one report's "judged by eye" line aloud. | Imported into a mm file: the runner warns about units. Stance not pasted: the report says *Balanced*. Students looking for old towers: layers under `runs::tower`. |
| 13 | Measure | Press `→` five times. Land step 4: the limit is in **your** skill. | |
| 14 | First measure | Five minutes. Everyone pastes the same row. | Row pasted below the table instead of replacing *(none yet)*: the skill may still say it has no measures. |
| 15 | Challenge | Pairs, 25 min. Read the rules aloud twice. At 20 min: "best tower and its receipts, now". Collect gfa, sun lost and beyond-plot per pair, from receipts. | Numbers from Claude's summary rather than the receipts: ask for the receipt. Towers that lean or overhang out of the plot to win: the scoreboard strikes them. |
| 16 | Scoreboard | Type each pair in as they call out (pair name, m², %, m). | |
| 17 | The winner | Put the winner on the projector in Rhino (perspective, then from the river: `Site::River views`). Ask: is it calm? Is it noticed? Read the Strathern line. Ask for one thing it got away with. | The room defends the winner: good, ask which measure would have caught it. |
| 18 | Menu | Two minutes. Connect each measure back to the slide 4 groups. Mention the terraces example (notes) if anyone picked terraces. | |
| 19 | Choose what counts | Pairs, 35 min. Check each pair wrote a sentence for its limit before running. | Limits copied unchanged from the contract: ask why that number. Nothing passes: say it's a finding, not a bug; the skill mustn't loosen the limit. |
| 20 | Crit | Two or three pairs, both questions. Push on the second: every answer is a new measure or a judgement that stays human. | |
| 21 | Ladder | Press `→` once for Sessions 3–4. Take-home: a contract for a measure that isn't on the menu. | |

## What to expect in the challenge

Measured with the kits (Rhino 9, London, the site as built):

- **Height is free above about 20 floors.** On 21 March the sun in London is low (about 38° at noon), so a tower's shadow already reaches past the park by about 70 m of height. A 20 × 20 m tower loses 7.2% of the park's sun at 8 floors, 12.6% at 12, 18.7% at 20, and 18.79% at 24, 40, 60 and 80 floors alike.
- **The footprint decides.** At any height above that: 20 × 20 m 18.8%, 21 × 21 m 19.75% (passes), 22 × 22 m 20.7% (fails). Orientation matters too: 14 m east-west × 30 m north-south loses 18.1%, the same footprint turned the other way 23.2%.
- **The best tower found:** 80 floors (the slider's maximum, 280 m) on an 18 × 18 m base that widens upward to 30 m (`taper = 1.66`): 46,815 m², 18.4% sun lost, inside the plot. A straight 21 × 21 m × 80 floors gives 35,280 m². The widest box that passes, 30 × 30 m, only manages 11 floors (9,900 m², 19.0%).
- So expect the leaders to push floors to 80 and then tune the footprint and the taper. That is the point of slide 17: the winner is a 280 m tower that gets wider as it rises, next to a park, and the measure is happy with it. Ask whether it is *calm*.
- **Leaning south**, away from the park, quickly leaves the plot (`beyond_plot_m`): a 20 m lean over 30 floors is 15 m out. The plot rule is what stops that exploit.
- **Twisting** changes little for the park; it raises `river_view` and leaves sliver terraces (`terraces`: 298 m² in pieces of at most 2.6 m²).

## Likely problems

- **No Rhino tools in Claude.** The MCP server isn't connected to the desktop app (setup checklist). Not fixable in class in a minute: pair them with a neighbour.
- **"No module named ladybug…"** on Rhino 9: the Ladybug installer gap (setup checklist). Pair them up for Part 2.
- **Units warning.** The site was imported into a millimetre file. Close it and File › Open `site/site.3dm`.
- **Two Rhinos.** The MCP started its own. Use that one, or close both and let it start one.
- **A measure gives 100% sun lost, or empty outputs, with "was given nothing".** An input wasn't given (usually the tower layer name is wrong). The layer is `runs::tower::<label as the runner wrote it>::mass`, e.g. `A-quiet-slab`.
- **Permission prompts on every run.** `run_python` asks each time by design. Students may choose "allow for this session" during the challenge; say what that means (any script, not only the runner).
