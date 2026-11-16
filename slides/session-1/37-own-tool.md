<!-- layout: task | where: code-yours | time: 25 min -->
<p class="kicker">Your turn · spec first</p>

# Design a tool without writing code

1. **Take the tool-spec kit** (prompt below).
2. Pick something small and exact: *stair fit, brick coursing, ramp gradient, parking count.*
3. Copy `tools/TEMPLATE.md` to `tools/<your_tool>.md` and fill it in. Work out **three test cases by hand**.
4. New session: run `/tool-builder`. It questions your contract first.
5. A test fails? Is the **code** wrong, or your **contract**?

<div data-widget="takeaway" data-kit="tool-spec"></div>

<details><summary>Example contract: tools/stair_check.md</summary>
<div data-widget="file" data-path="kits/tool-spec/tools/stair_check.md" data-render="markdown" data-title="tools/stair_check.md"></div>
</details>

<!-- notes -->
**The idea.** You've used tools. Now you design one, without writing code. A tool's **contract** is a plain-language description of what it takes (inputs, units, ranges), the rule it applies, and what it returns. Writing the contract is the authorship. Claude writes the code to match it, and *your* hand-worked test cases decide whether the code is right.

You don't need to read the code. The most useful moment comes before any code exists, when `/tool-builder` questions your contract. It might point out rounding you didn't specify, a missing unit, or a test case your own rule doesn't actually produce.

**Good sizes:** stair fit (see the example), brick coursing, ramp gradient, parking count, a room-area schedule. **Too big:** anything that needs geometry, images or the internet.

**Why it matters.** When a test fails, ask: who was wrong? Sometimes it's the code. Often it's the contract, which said something you didn't mean. Finding that out on paper is much cheaper than finding it on site.

**Try it yourself.** Give your finished tool to your partner without explaining it. Can they use it from the contract alone?
