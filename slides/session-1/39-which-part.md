<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · All together</p>

# Which part was it?

<div data-widget="figure" data-name="which-part"></div>

> For each line: which of the six parts was responsible? Call it out before the answer appears.

<!-- notes -->
**The idea.** When something goes wrong in an agentic system, the first useful question is *which part* was responsible. Each part fails in its own way, and each has its own fix:

- **The LLM** writes what's likely. If it says it rolled a 7, check the receipt: no tool ran, so nothing was rolled.
- **Context** is only what you wrote down. If a new session forgot your units, they weren't in your `CLAUDE.md`.
- **A skill** only holds what it says. If nothing said "roll exactly once", re-rolling until it liked the answer wasn't against any rule.
- **A rule can still be ignored.** Even when the skill says "roll once", the model may roll twice: a rule is read, not enforced. If it really matters, make it hard to break with a permission, and check the receipt.
- **You** set the goal. If "good" was never defined, the agent picked its own meaning and stopped there.
- **A tool** does exactly what it promises. Refusing `1,5` isn't a failure: the tool couldn't be sure what you meant, so it said so instead of guessing.

And the app? It's the frame all six parts sit in. A permission prompt comes from the app, but the leash it holds is the one *you* set.

**Why it matters.** "The AI got it wrong" doesn't tell you what to change. "The skill had no rule for that" does. You'll use this question for the rest of the course, whenever a run surprises you.

**Try it yourself.** Think back to a moment today when Claude did something you didn't expect. Which part was it, and what would you change: the brief, the skill, the context or the tool?
