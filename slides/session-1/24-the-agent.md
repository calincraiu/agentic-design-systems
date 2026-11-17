<!-- layout: section | where: app -->
<p class="kicker">Part 1 · The parts, 3 of 5</p>

# The agent

<p class="lead">An LLM that acts, looks, and decides again.</p>

<div data-widget="figure" data-name="parts" data-ghost data-start="0" data-focus="3" class="map"></div>

<!-- notes -->
**In this section.** Put the LLM and the tools together and let the LLM decide when to use them, and you have an **agent**. The dashed line in the diagram is that combination: an LLM that can ask a tool for something, read the result, and decide what to do next. The **app** runs that loop: it carries each request to the tool and brings the result back. That's why the whole diagram sits inside a frame labelled *the app*.

Five short slides: what makes an agent different from a single answer, how it actually runs a tool on your laptop, a dice run in your own folder where nobody says in advance how many steps it will take, how an agent knows when to stop, and how much freedom you give it.

**A note on words.** We say the agent "decides", "looks" or "thinks it's done". That's shorthand: underneath, it's the model writing the next likely piece of text. But don't swap one myth for another. "Just predicting the next word", done at this scale, is how it can write a working program or a sensible plan. Powerful, and still only text.
