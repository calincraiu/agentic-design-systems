<!-- layout: diagram | where: code-yours -->
<p class="kicker">Part 2 · Demo</p>

# You are the client

<div data-widget="figure" data-ghost data-name="loop" data-start="1"></div>

> Demo, in the Code tab: `/tower-designer`, with **the wish you gave Chat at the start**: calm, but noticed from the river, next to a park.

<!-- notes -->
Clients don't brief in eight numbers. They say something like "calm, but noticed from the river", and getting from those words to the tool's inputs is the design problem. The `tower-designer` skill runs a loop for it, and the colours in the diagram show who does each step:

1. **You describe** the tower in your own words.
2. **The agent asks** the three questions whose answers would change the design most, then **stops and waits**.
3. **You answer.** The agent writes a short **brief** with your words, how it read them, what it assumed, and the limits.
4. **The tool builds three** different strategies and checks each one against the limits.
5. **The agent reports** the trade-offs, and **you choose**. If you're not satisfied, change the brief, the skill or the tool and go round again.

The brief records how your words were interpreted, so you can disagree with the reading rather than only with the result. The pause in step 2 is written into the skill on purpose, so that the design doesn't go ahead on the agent's guesses about what you meant.

Run `/tower-designer` with a wish that pulls in two directions, such as "very tall, but it mustn't overshadow the park". Read the brief before you look at the images.
