<!-- layout: section | where: app -->
<p class="kicker">Part 3 · A skill that judges</p>

# A skill wires tools, in words

<p class="lead">Which measures to run, and what counts as passing. Written once, used every time.</p>

<div data-widget="figure" data-name="chain" data-start="5" data-ghost class="map"></div>

<!-- notes -->
In a Grasshopper definition you wire components together. A skill does the same one level up: it says which tools to run, in what order, with which inputs, and what to do with the results. The wiring is in plain words, and the agent follows it.

So far you've chained the tools by asking, one message at a time. That only lasts as long as the conversation. Every message sends the model the **whole conversation** so far, including the output of every tool run, and the model can only take in a fixed amount of text at once: the **context window**. When a conversation nears that limit, the app **compacts** it, replacing older parts with a summary, and details from early on can blur. A new session starts clean, and Claude reads `CLAUDE.md` and the skills fresh each time. So anything that must last from one task to the next, such as which measures you trust and where your limits are, belongs in a file. For a way of working, that file is a skill.
