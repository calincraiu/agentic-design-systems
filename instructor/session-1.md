# Session 1: instructor notes

**Aim.** Students can tell apart an LLM, a tool, an agent, a skill and context, because they have seen each one do something the others can't. By the end, they have **their own folder** with a `CLAUDE.md`, the add and dice kits, a skill they wrote, a design stance and (if time allows) a first tool contract. No Rhino in this session.

**Two folders, said early and often:** the course folder is the tutorial: followed, run and read, never built in. Their own folder is their project, and it is where all authorship happens.

**The slide notes are for students.** Each slide's notes (`N`, and reading mode) explain the slide to a student revising after class. Everything meant only for you (what to press, what to ask the room, what to watch for) is in the **Slide by slide** table below. This folder is left out of the student zip.

## Run-sheet (about 3 h 55)

The slides are `slides/session-1/` in the course app (`uv run course`): 39 sheets. They alternate between the app (concepts, widgets) and Claude's Chat and Code tabs (polls, demos and student work). The chip at the bottom right of each slide says where the students should be working.

The session is in chapters, and each one opens with a **section slide** (big title, one lead line). Part 1 meets the parts of the system one at a time, in the order the `parts` diagram builds them: **the LLM, the tool, the agent, the skill, context**, and then you. On each Part 1 section slide, the diagram shows the parts so far, with the rest ghosted. Press `→` once to draw the new part, then move on. Each section uses both running examples: adding up (exact) and rolling dice (fair).

| Time | Slides | Activity | Where |
|---|---|---|---|
| 0:00–0:10 | 1–2 | Title, then the hook: eight towers, "How would you know?" | App |
| 0:10–0:25 | 3–6 | **Groundwork.** Chat vs Code (the `hello.md` demo), text files, two folders. Anyone without the app: `/setup`, `/start` in the course folder | App + both tabs |
| 0:25–0:45 | 7–12 | **The LLM.** Tokens, and the one-piece-at-a-time loop; the room finishes the sentences (Sullivan); in-your-head poll, three questions; fairness poll | App ↔ Chat |
| 0:45–1:00 | 13–16 | **The tool.** `add.py` and `1,5 2`; a command taken apart; `dice.py` and the repeats count | App ↔ Chat |
| 1:00–1:15 | 17–21 | **The agent.** Chat vs agent loop; guess, then roll until a double, twice; "good result" vs "total over 30"; the leash poll | App ↔ your folder |
| 1:15–1:30 | 22–24 | **The skill.** `add-up` on the poll's sum; `tie-breaker` on the poll's six architects | Your folder |
| 1:30–1:40 | 25–27 | **Context.** Context stepper and the commentator line; six parts | App ↔ your folder |
| 1:40–2:20 | 28–31 | **Your turn.** Students start their own folder, write `CLAUDE.md`, take the add + dice kits, write their own skill | Their folder |
| 2:20–2:35 | | Break | |
| 2:35–2:55 | 32–34 | **A tower.** Tower explorer (words with no slider); `/tower-designer` demo with your own wish | App ↔ your folder |
| 2:55–3:25 | 35 | Students take the tower kit, write a stance, run both stances on one shared wish | Their folder |
| 3:25–3:45 | 36–37 | **Your own tool.** Spec first: fill in `TEMPLATE.md`, `/tool-builder` | Their folder |
| 3:45–3:55 | 38–39 | Crit: "What could your skill **not** change?" Then the ladder, and the take-home | App |

**Presenting.** `→` reveals the next part of a diagram before moving to the next slide, `←` hides it again. `N` opens the notes, `G` shows all slides, `R` switches to reading mode, `D` toggles dark/light, `F` goes full screen, and `?` (or the **Keys** button at the top right) lists them all. For a bright projector, open the app once with `?theme=light` on the address (for example `http://127.0.0.1:8765/?theme=light`), and it remembers.

**If you're behind:** move *Your own tool* (slides 36–37) to the start of Session 2, where it leads into *Tool* and *Measure* on the ladder. Keep the stance: it's the authorship, and it sets up the crit. Slides 8–9 (tokens, the loop) take about three minutes together, inside the LLM block; if you're short, give each one minute, because the vocabulary matters more than the detail. The command slide (15) can be shown quickly: the students meet commands again in every "Behind the scenes".

**Try these in Chat beforehand.** Four asks depend on how Chat behaves on the day: the long sum and "how did you work that out?" (slide 11), the fairness poll (12), `1,5 + 2` (14), and 20 dice rolls (16). Each slide still makes its point if Chat behaves "well", and the notes say how. Still, know what you'll get before the room does.

## Your demo folder

Do the demos in **your own folder**, built with the same take-away kits the students use, not in the course repo. Students then see exactly what they'll do. Before class: make an empty folder, write a short `CLAUDE.md`, copy in the `add`, `dice` and `tower` kits, and run `/tower-designer` once with a wish of your own so its `runs/` is ready.

For the hook slide, the app's gallery shows the course folder's `runs/`. To show your own prepared runs instead of the contact sheet, swap the `contact` widget for `<div data-widget="gallery"></div>` in `02-hook.md`, then either build a few towers in the explorer beforehand, or copy your demo folder's `runs/` into the course folder's `runs/`.

**The take-away prompts show *your* path when projected.** That's expected: the app finds the course folder on the computer it runs on, so each student's own app shows their own path. Say it out loud on slide 35 (the first prompt students paste): copy it from your own app, not from the screen. Slide 28 uses a zip instead, so nothing there depends on a path.

## Slide by slide

| # | Slide | Do / say | Watch for |
|---|---|---|---|
| 3, 7, 13, 17, 22, 25, 28, 32, 36 | Section slides | Read the lead line aloud. On Part 1 sections, press `→` once to draw the new part ("this is what we add now"). On 30 and 34 the map is already whole: point along it (words → numbers → tower → back; contract → tests → code → "which is wrong?"), no key press. Thirty seconds, then move on. | |
| 1 | Title | Ask the question and leave it hanging. Don't explain the skyline. | |
| 2 | Hook | Let the room argue for a minute. Expect "elegant", "grounded", "dramatic"; ask what each word would be measured with. Don't explain the tool yet: Part 2 comes back to it. | |
| 4 | Chat vs Code | Press `→` three times first: Chat's own space, Claude inside your folder, the **Allow?** gate. Then, with your demo folder open in Code, type **"Make a file called hello.md that says hello."** in both tabs. Chat shows text or a download; Code asks permission. Then open the folder in Explorer/Finder: the file is there. "Same words, same Claude: only one touched my computer." Have everyone open both tabs now. | Chat may offer a downloadable file. That's fine: it's still not in your folder. Delete `hello.md` afterwards. |
| 5 | Text files | Open `kits/add/.claude/skills/add-up/SKILL.md` in Notepad on the projector. "This is the know-how you'll see change Claude's behaviour in an hour. It's eighteen lines of English." | Hidden `.claude` folder: Cmd + Shift + . (Mac), View › Show › Hidden items (Windows). |
| 6 | Two folders | Open with why: Claude works inside one folder, so lesson and project are kept apart. Say it early and often. The chip at bottom right says where to work. | Anyone working in the course folder. |
| 8 | Pieces | Press `→` three times: the sentence cut into pieces, a long word cut into several, then the dashed "?". Say it plainly: "All it ever writes is the next piece." The point is one word, **token**, so keep it to a minute. | Someone asks how it *picks* the next piece: "That's two slides on." |
| 9 | One at a time | Press `→` four times: round 1, round 2 (the new piece goes back in), round 3, then "no plan, no looking ahead". Ask: "If the first piece was a strange one, what happens to everything after it?" It builds on it. Say *autoregressive* once, then move on. | Don't get into the maths. If someone asks what "likely" means, that is the next slide. |
| 10 | LLM writes | The bars are the "choose" step of the loop you just saw. Press `→` after the room finishes each sentence: the bars show the likely endings (made-up weights, as the figure says). The room says "A house has walls, a floor, and a…" and "Form follows…" together. Then ask who first wrote "form follows function". Most say Le Corbusier, Mies or the Bauhaus. Reveal: Louis Sullivan, "The Tall Office Building Artistically Considered", 1896. "You just did what an LLM does: fast, fluent, from pattern. Two endings were right, the author was wrong, and it all felt the same." | Someone may know Sullivan: good, ask how they know. That's knowledge, not pattern. |
| 11 | In your head | Everyone asks the three questions in a **fresh chat**, pastes the long-sum answer into the widget (or calls it out and you type), then **Add with the tool**. Then read out one or two answers to "how did you work it out?". Land it: the explanation is generated text too, not a record. | Chat may be right every time, or quietly run code. If it ran code, that's the lesson ("it reached for a tool"). Have a harder sum ready (longer numbers, or 25 room areas). |
| 12 | Fairness poll | Everyone asks in a **new conversation** and calls out the name; click a name per answer. Then **Roll the dice the same number of times**, then **Roll again** two or three times. Land it: a wobble that moves is chance, a lean that stays is bias. | If Chat barely leans, add names, or put the most famous first. If it runs code, ask: "how do you know that was fair?" |
| 14 | Add tool | Read `add.py` aloud: it's twenty lines, and removing the fear of code is the point. Type `0.1 0.2`, then `1,5 2` (it refuses). Ask the room what Chat says for "1,5 + 2". "A tool can say *I can't*. An LLM always answers." | |
| 15 | Command | Press `→` four times: run it, this file, these inputs, what comes back. | |
| 16 | Dice tool | Everyone asks Chat for 20 rolls and counts back-to-back repeats; you roll 20 with the widget and count. A fair die averages about 3 in 20. Collect a few counts from the room. | Chat may run code (then its count looks normal: it used a tool). Lists with 0 or 1 repeats are the usual result. |
| 18 | Agent vs chat | Press `→` five times: Act, Look, Decide, the dashed loop-back, Report. "Chat answers once. This keeps going until *it* decides it's done." Stop on the loop-back and ask: how many times round? Nobody said. | |
| 19 | Agent | Ask everyone to write down a guess first (a number of rolls until a double). Run the demo, then run it again. "Different number of steps. Nobody wrote the plan in advance." Collect a few guesses: most are 2 or 3, the average is 6. | Claude may write a small loop instead of calling the tool repeatedly. That's still the agent deciding how: point it out. |
| 20 | When done | Run A, then B. Then press `→` three times: the rolls, A's line at 30, B's "?". For B, wait to see whether it asks what "good" means or invents a meaning. Then open the commands each one ran and read them against its summary: "trust the receipt". Ask: what would you have to decide before B could be A? | It may refuse to start B and ask what "good" means. That's the best outcome: say so. If it stops after one roll, ask who decided that was good. |
| 21 | The leash | Read the four items one at a time for a show of hands (expect it to split on overwrite, the four-hour job and the email). Press `→` to build the four levels. "Where do the kits sit?" Level 3. Point back to the first permission prompt students saw. | Nobody puts a hand up for anything: ask what would change their mind (a scratch folder? a backup?). |
| 23 | `add-up` | Click through the anatomy. In your folder, run `/add-up` with the poll's long sum (from slide 9). Put it next to Chat's answer: "same question, now you can see how". Then "2 + 2". Ask: is "never in its head, even 2 + 2" sensible? | |
| 24 | Tie-breaker | Run `/tie-breaker` with the six architects from the poll. Ask for a re-roll, then ask which one it prefers. "The lean is still in the LLM. The skill keeps it out of the decision." | |
| 26 | Context | Step through to step 5: what survives a new session. Then the commentator line. | Needs a **new session**. Delete the line afterwards. |
| 27 | Six parts | Press `→` once to draw *you*. Checkpoint: point at a part and ask for today's example. | |
| 29 | Your folder | Pairs or solo. Suggest the rule "never make up a number or a roll". Walk the room: check each student has the folder open in the **Code tab**, not the course folder. | Downloads, OneDrive, iCloud. Anyone working in the course folder. |
| 30 | Add the kits | Copying by hand, no Chat. Show it once: download the zip, unzip, drag `tools` and `.claude` into your folder. Say it out loud: turn on hidden items first. | `.claude` is hidden, so it gets left behind (Windows: View › Show › Hidden items; Mac: Cmd + Shift + .). `tools` nested inside another folder after unzipping. |
| 31 | Your skill | Pairs. Let Claude make the file; the students edit the words. | The agent may simply *say* it rolled a 7. Good discussion: the tool can't, the LLM can still write it. |
| 33 | Tower tool | Ask for a one-sentence wish from the room, then try to set it with the sliders live. Collect the words that had no slider. **Build with the tool**, then **Build the same again**. | |
| 34 | You are the client | Press `→` to build the loop step by step. Demo `/tower-designer` with a wish of your own that pulls two ways. Answer its questions honestly, read the brief aloud, then open the gallery. | The agent skipping the questions. It shouldn't (the skill says stop). If it does, ask the room why the pause matters. |
| 35 | Stance | Pairs agree on one wish and each run their own stance. If time allows, put two galleries side by side on the projector. | A run labelled `tower-designer` in the gallery: the name in the copied skill wasn't changed. |
| 37 | Own tool | Ask: "When a test fails, who was wrong?" | Tools that are too big: geometry, images, the internet. |
| 38 | Crit | Each pair shows their gallery or tool and answers both questions. Press `→` twice to bring up the tool and then you. | |
| 39 | End | Press `→` three times: what you climbed today (Context, Skill, the first Tool contract), what Session 2 adds (Tool, Measure), then the long way up (Workflow). Read the take-home aloud: one thing no metric captured. Add: their own folder keeps everything; the course folder is replaced each session. | Anyone who says they have nothing to bring: ask what they wanted the tower to do that no slider could. |

## Teaching the own tool

The point is that **authoring a tool means authoring its contract**: inputs, ranges, the rule in words, the output, and test cases worked out by hand. Students don't need to read the code: `/tool-builder` writes it, then runs *their* test cases. Its most useful moment is step 2, when it questions the contract before writing anything: unclear rounding, a missing unit, a test case the rule doesn't produce.

Good sizes: stair fit (the worked example), brick coursing, ramp gradient, parking count, room-area schedule. Too big: anything needing geometry, images or the internet.

## What the tower can't measure (seeds for Session 2)

Whatever wish students bring, these come up. Collect them in the crit: they're where Session 2 starts.

- **Terraces and outdoor space:** no metric for them. The perfect Session 2 seed.
- **Views and orientation:** where the top floor faces, what it looks at.
- **Visibility and memorability:** "seen from the river", "a landmark".
- **Cost and structure:** overhangs are measured (`max_cantilever_m`), their cost and risk aren't.
- **Daylight and fairness between floors:** shadow is one fixed sun position on the ground only.
- **Shape limits:** taper is linear, so a tower can't "stay thin and flare near the top". Wanting that is a reason to change the *tool*, not the skill.

## Likely problems

- **Students work in the course folder.** In the student copy, Claude is told not to edit there, and edits are denied. If someone is stuck, check which folder their Code tab has open.
- **The take-away prompt doesn't copy the hidden `.claude` folder.** Ask Claude to list `.claude/skills/` afterwards. Fallback: the "download the kit as a zip" link under each prompt.
- **The take-away prompt has the wrong path.** They copied it from the projector. Copy it from the app on their own computer; the prompt also tells Claude to ask if the folder doesn't exist.
- **A new skill doesn't show up.** Start a new session. If it still doesn't, check the folder is directly in `.claude/skills/<name>/` and the file is called `SKILL.md`.
- **Students can't find `.claude/`.** Dot-folders are hidden in Finder and some file windows. Use the app's file pane, or ask Claude to open or copy the file.
- **The course app stops.** Started with `/start`, it lives as long as that Claude session. Run `/start` again, or use the double-click launcher.
- **Synced folders (OneDrive, iCloud).** These usually work, but can be slow or lock files. Prefer a local folder.
- **Permission prompts.** Each kit's `.claude/settings.json` pre-approves `uv run tools/...`. Anything else prompts, and that's worth a sentence: *the agent asks before acting outside its lane*.
- **Two skills with similar descriptions.** Call them explicitly (`/tower-good-neighbour`) rather than relying on the agent to pick one.
- **The gallery doesn't update.** It's rebuilt after each run, but the page needs a refresh.
