<!-- layout: diagram | where: code-yours -->
<p class="kicker">Part 2 · Demo</p>

# You are the client

<div data-widget="figure" data-ghost data-name="loop" data-start="1"></div>

> Demo, in the Code tab: `/tower-designer`, then describe a tower you would actually want.

<!-- notes -->
**The idea.** A client never talks in eight numbers. They say "something calm that still gets noticed from the river". Getting from those words to the tool's numbers *is* the design problem. The `tower-designer` skill runs a loop for it, and the colours show who does each step:

1. **You describe** the tower in your own words.
2. **The agent asks** the three questions whose answers would change the design most. Then it **stops and waits**.
3. **You answer.** The agent writes a short **brief**: your words, how it read them, what it assumed, and the limits.
4. **The tool builds three** different strategies and measures each one against the limits.
5. **The agent reports** the trade-offs. **You choose.** Not happy? Change the brief, the skill or the tool, and go round again.

**Why it matters.** The brief writes down *how your words were read*, so you can question the reading instead of just the result. And the pause in step 2 is deliberate: the human checkpoint is part of the workflow's design.

**Try it yourself.** Run `/tower-designer` with a wish that pulls two ways, like "very tall, but it mustn't overshadow the park". Read the brief before you look at the images.
