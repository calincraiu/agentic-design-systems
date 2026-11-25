<!-- layout: task | where: code-yours | time: 10 min -->
<p class="kicker">Part 1 · A Grasshopper tool · your turn</p>

# Claude runs your tool

1. **New session:** *"Use the grasshopper skill to add 12.5 and 30 with my sum tool."*
2. **Read** the three lines before you allow them.
3. **Open** the receipt in `runs/`.
4. **Ask** for 2000 + 1.
5. **Ask** Claude to run the test cases in `sum.md`.

<details><summary>Your sum won't run, and the clock is ticking?</summary>
<div data-widget="takeaway" data-kit="sum"></div>
</details>

> **You're done when** you have a receipt and a refusal. Then your setup works: Rhino, the MCP, the runner, and your tool.

<!-- notes -->
#### What you're building
Nothing new: Claude runs the tool you just built. A receipt and a refusal prove that the whole setup works: Rhino, the MCP, the runner and your file.

#### Steps
1. **Start** a new session and ask Claude to add 12.5 and 30 with your sum tool. *The first run can take a few seconds while Grasshopper loads.*
2. **Read** the permission prompt: it should be the three lines from the previous slide, with your folder's path, `sum.gh` and `{"a": 12.5, "b": 30}`. Allow it.
    - If it's anything else (a script that searches the canvas or moves sliders): deny it and point Claude to the `grasshopper` skill.
3. **Open** the receipt in `runs/`, e.g. `runs/2026-11-28_101504_sum.json`.
4. **Ask** for 2000 + 1. *It's outside your 0–1000 range, so the runner refuses before anything runs.*
5. **Ask** Claude to run the test cases in `sum.md`.
    - If the runner says the tool has no inputs or no outputs: a nickname is missing its `in:` or `out:`.
    - If it can't find the file: check it is `tools/sum/sum.gh`, directly inside your folder.
    - If yours won't run in time: take the `sum` kit (on the slide), a finished copy of the tool and its contract. Compare the two afterwards.

#### Background
The receipt records which inputs you gave, which kept the value saved in the definition, what came out, and when. It's the same habit as Session 1: Claude's explanation is text it wrote, and the receipt is the record.

If a test case fails, ask who was wrong: the definition (a wire to the wrong input, a slider rounding to whole numbers) or the contract (a sum worked out wrongly). Fix that one. Nothing you change on the canvas reaches Claude until you save the file.
