<!-- layout: task | where: rhino | time: 20 min -->
<p class="kicker">Part 1 · A Grasshopper tool · your turn</p>

# Build the adding tool

1. **Place** two Number Sliders, an Addition and a Panel. Wire them up.
2. **Set** each slider: 0 to 1000, two decimal places.
3. **Name** them `in:a`, `in:b` and `out:sum`.
4. **Save** it in your folder as `tools/sum/sum.gh`.
5. **Copy** the template to `tools/sum/sum.md`. Fill in the ranges and two test cases.

> **You're done when** `tools/sum/` holds `sum.gh` and `sum.md`, and the Panel shows the sum of your two sliders.

<!-- notes -->
#### What you're building
`sum.gh`: two numbers in, their sum out, plus its contract `sum.md`. It's Session 1's `add.py` as a Grasshopper definition, and your first tool.

#### Steps
1. **Start** Grasshopper: type `Grasshopper` in Rhino, then File › New Document.
2. **Place** two Number Sliders, one Addition and one Panel. *Double-click an empty part of the canvas, type the name (`slider`, `addition`, `panel`), press Enter.*
3. **Wire** them: drag from an output (the half-circle on a component's right) to an input (on its left). Each slider into one input of Addition, its result into the Panel.
4. **Set** each slider: right-click › **Edit…** › two decimal places, Min 0, Max 1000. *This range is what the tool will accept.*
5. **Rename** the sliders `in:a` and `in:b`, and the Panel `out:sum`: right-click, type in the field at the top of the menu. *The `in:` and `out:` names are what make it a tool.*
6. **Save** it: File › Save As, make the folder `tools/sum` inside your own folder, save as `sum.gh`.
7. **Copy** `tools/grasshopper/TEMPLATE.md` to `tools/sum/sum.md` and fill it in, with two test cases worked out on paper.

#### Background
For a tool this small, most of the contract takes one line per section: who would use it, the two inputs with their range, "adds a and b", the output. A good pair of test cases is one sum, such as 12.5 + 30, and one value the tool should refuse. *What it can't tell you* is worth a sentence: it adds 3 m and 250 mm without noticing the units differ.

When Claude runs the tool, anything outside a slider's range, or with more decimal places than it allows, is refused.
