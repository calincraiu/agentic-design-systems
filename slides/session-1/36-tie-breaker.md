<!-- layout: split | where: code-yours -->
<p class="kicker">Part 1 · The skill</p>

# A skill can keep the LLM fair

<div class="cols" markdown="1">
<div data-widget="file" data-path="kits/dice/.claude/skills/tie-breaker/SKILL.md" data-title=".claude/skills/tie-breaker/SKILL.md"></div>
<div markdown="1">

The poll showed that the LLM leans. This skill **never lets it choose**: it rolls the dice tool, exactly once.

> In your folder: `/tie-breaker` with **the poll's six architects**. Then ask for a re-roll, and ask which one Claude prefers.

</div>
</div>

<!-- notes -->
`tie-breaker` has the same parts as `add-up`: a description, a few steps and some rules. It turns the problem from the poll into a fair procedure. The options are numbered, a die with that many sides is rolled once, and the number decides.

Two of the rules do most of the work. *Roll exactly once*, because if you can re-roll until you like the result, the outcome is your own choice made slowly, not a fair draw. The skill points that out and leaves any re-roll to you. *Give no opinion*, because otherwise the model's preferences come back in through its comments on the result.

The lean from the poll is still in the model, as you saw when you asked which architect it prefers. The skill keeps it out of the decision, so each architect had exactly one chance in six.

A skill is where you write down a process you trust, such as how to make a fair choice, when to check, or when to ask before acting. It then applies every time the skill runs, as long as the model follows it, which isn't guaranteed (see the notes on the next slide).

Use `/tie-breaker` to decide your crit order with your partner, then try to talk it into a re-roll.
