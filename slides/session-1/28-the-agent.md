<!-- layout: section | where: app -->
<p class="kicker">Part 1 · The parts, 3 of 5</p>

# The agent

<p class="lead">An LLM that acts, looks, and decides again.</p>

<div data-widget="figure" data-name="parts" data-ghost data-start="0" data-focus="3" class="map"></div>

<!-- notes -->
An **agent** is an LLM that can use tools and decides for itself when to use them. It asks a tool for something, reads the result and decides what to do next. The dashed line in the diagram marks that combination. The **app** runs the loop, carrying each request to the tool and bringing the result back, which is why everything sits inside the frame labelled *the app*.

The section covers how an agent differs from a single answer, how it runs a tool on your laptop, a dice run in your own folder where the number of steps isn't fixed in advance, how an agent decides it has finished, and how much freedom you give it.

The slides say the agent "decides", "looks" or "thinks it's done". That is shorthand for the model writing the next likely text. The shorthand shouldn't make you dismiss it either. Producing likely text at this scale is enough to write a working program or a reasonable plan.
