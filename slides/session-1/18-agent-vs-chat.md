<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The agent</p>

# Chat answers once. An agent keeps going.

<div data-widget="figure" data-name="agent-loop" data-start="1"></div>

<!-- notes -->
**The idea.** Ask Chat something and you get one answer, then it waits. An **agent** is built differently. You hand it a *goal*, and it goes round a loop on its own:

1. **Act.** It uses a tool: runs a command, reads a file, makes something.
2. **Look.** It reads what came back.
3. **Decide.** Is that good enough? If not, it acts again, using what it just learned. If so, it stops and reports.

Two parts of that loop are the LLM (looking and deciding). One is a tool (acting). You appear only at the two ends: you set the goal, and you read the report.

**Why it matters.** Notice what isn't in the diagram: a list of steps. You didn't write one, and neither did Claude, in advance. The number of rounds depends on what each result turns out to be. Design is full of loops like this (try, look, adjust), and an agent can run one quickly. But the *deciding* is still the LLM's judgment. The next slides are about what that means for you.

**Try it yourself.** Think of a job you do by trying, looking and adjusting: tuning a stair, nudging a facade grid, checking a drawing set. Which step would you hand over, and which would you keep?
