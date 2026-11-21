<!-- layout: task | where: code-yours | time: 10 min -->
<p class="kicker">Part 1 · Tool · your turn</p>

# Run a Grasshopper tool

1. **Ask:** *"Use the grasshopper skill to add 12.5 and 30."*
2. **Read** the three lines before you allow them.
3. **Open** the receipt in `runs/`.
4. **Ask** for 2000 + 1.
5. **Open** `tools/sum/sum.gh` in Grasshopper. Find `in:a`, `in:b`, `out:sum`.

> **You're done when** you have one receipt and one refusal, and can say where the 0–1000 limit comes from.

<!-- notes -->
The first run may take a few seconds while Grasshopper loads. After that, a run like this takes well under a second.

When the permission prompt appears, read the script. It should be the three lines from the previous slide, with your folder's path, `sum.gh` and `{"a": 12.5, "b": 30}`. If Claude sends anything else, such as a script that searches the canvas or moves sliders itself, deny it and point it to the `grasshopper` skill.

The receipt is a small JSON file named after the time and the tool, for example `runs/2026-11-28_101504_sum.json`. It records which inputs you gave, which kept the value saved in the definition, what came out, and when. It's the same habit as Session 1: the explanation in Claude's reply is text it wrote, and the receipt is the record.

2000 is outside the slider's range of 0 to 1000, so the runner refuses before anything runs, and tells Claude what the allowed range is. The range lives in the slider itself: right-click a slider in Grasshopper and look at its Min and Max. Changing those numbers changes what the tool accepts. That's a change to the tool, so it goes in its contract too.

To open the file, start Grasshopper from Rhino (type `Grasshopper`), then File › Open. Nothing you change in the canvas reaches Claude until you save the file.
