<!-- layout: split | where: code-yours -->
<p class="kicker">Part 1 · The skill</p>

# A skill can keep the LLM fair

<div class="cols" markdown="1">
<div data-widget="file" data-path="kits/dice/.claude/skills/tie-breaker/SKILL.md" data-title=".claude/skills/tie-breaker/SKILL.md"></div>
<div markdown="1">

The poll showed that the LLM leans. This skill **never lets it choose**: it rolls the dice tool, exactly once.

> Demo: `/tie-breaker` with **the poll's six architects**. Then ask for a re-roll, and ask which one Claude prefers.

</div>
</div>

<!-- notes -->
**The idea.** This is your second skill, with the same parts as `add-up`: a description, a few steps and some rules. Its job is to turn the problem from the poll into a fair process. The options are numbered, a die with that many sides is rolled once, and the number decides.

Two of its rules are worth reading closely:

- **Roll exactly once.** If you could re-roll until you liked the answer, it wouldn't be a fair decision any more. It would be your decision, made slowly. The skill says so, and leaves the choice to you.
- **Give no opinion.** Otherwise the LLM's lean creeps back in, through its comments.

**The demo.** It's the poll's question again, and this time the answer is fair: each architect had exactly one chance in six. The LLM's lean hasn't gone anywhere. The skill simply keeps it out of the decision.

**Why it matters.** A skill is where you write down a *process* you trust, not just a task. Fairness, checking, asking before acting: these are decisions about how work should go. Once written, they hold every time the skill runs.

**Try it yourself.** Use `/tie-breaker` to decide your crit order with your partner. Then try to talk it into a re-roll. What does it say?
