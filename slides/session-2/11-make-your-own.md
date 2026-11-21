<!-- layout: task | where: rhino | time: 30 min | pairs -->
<p class="kicker">Part 1 · Tool · your turn</p>

# Make a floor-area tool

1. **Contract first.** Make a folder `tools/floor_area/`. Copy the template into it as `floor_area.md` and fill it in, with two test cases **by hand**.
2. **Build** it in Grasshopper: three sliders, two Multiplications, one Panel.
3. **Name** them `in:width`, `in:depth`, `in:floors`, `out:area_m2`. Ranges from your contract.
4. **Save** it in that folder as `floor_area.gh`.
5. **New session:** *"Run my floor_area tool on the test cases in its contract."*

> **You're done when** both test cases match, and a value outside your range is refused.

<!-- notes -->
This is a whole tool, built and specified by you, at the smallest size that still works. Its rule is short on purpose: the point is the contract and the naming, not the Grasshopper.

**Contract first.** The template is `tools/grasshopper/TEMPLATE.md`, from the `gh` kit. Width, depth and floors go in; floor area comes out. Decide the ranges before you build: what is the smallest and largest width that makes sense, in metres? Can floors be 2.5? The ranges you write become the sliders' Min and Max, and the runner refuses anything outside them. Work out your two test cases on paper, for example 20 × 20 m on 12 floors.

**Building it**, if Grasshopper is new to you:

- Start Grasshopper (type `Grasshopper` in Rhino), then File › New Document.
- To place a component, double-click an empty part of the canvas, type its name (`slider`, `multiplication`, `panel`) and press Enter.
- Right-click a slider and choose **Edit…** to set its rounding (whole numbers for floors, one decimal for metres), Min, Max and value.
- To rename a slider, right-click it and type the new name in the field at the top of the menu: `in:width`. Do the same for the Panel: `out:area_m2`.
- Drag from an output (the small half-circle on the right of a component) to an input (on the left) to connect them: width and depth into the first Multiplication, its result and floors into the second, and that result into the Panel.
- File › Save As: make the folder `tools/floor_area` inside your own folder, and save there as `floor_area.gh`.

If a test case fails, ask who was wrong: the definition (a wire to the wrong input, a slider rounding 3.5 to 4) or the contract (a test case you worked out wrong, a range that rules out a sensible building). Fix whichever it is, and save again.

If the runner says the tool has no inputs or no outputs, a nickname is missing its `in:` or `out:`. If Claude writes a different script from the three lines, or builds the definition itself, stop it: in this course, Claude runs tools and you build them.
