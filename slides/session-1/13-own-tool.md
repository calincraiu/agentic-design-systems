<p class="kicker">Your turn · spec first</p>

# Design a tool without writing code

You decide what a tool **takes** and what it **returns**. That's the authorship. Claude writes the code to match your contract, and your own test cases decide whether it's right.

<div class="cols" markdown="1">
<div markdown="1">

1. **Take the tool-spec kit** (prompt below).
2. Pick something small and exact: stair fit, brick coursing, ramp gradient, parking count, a room-area schedule.
3. Copy `tools/TEMPLATE.md` to `tools/<your_tool>.md` and fill it in. Work out **three test cases by hand**.
4. Start a **new session** and run `/tool-builder`. It will question your contract before it writes anything.
5. If a test fails, decide: is the **code** wrong, or your **contract**?

</div>
<div data-widget="file" data-path="kits/tool-spec/tools/stair_check.md" data-render="markdown" data-title="Example contract: tools/stair_check.md"></div>
</div>

<div data-widget="takeaway" data-kit="tool-spec"></div>
