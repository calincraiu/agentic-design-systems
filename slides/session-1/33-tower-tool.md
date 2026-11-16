<!-- layout: stage | where: app -->
<p class="kicker">Part 2 · A tower</p>

# Eight numbers in, a measured tower out

<div data-widget="tower" data-plot="20x20" data-require="height_m>60"></div>

> These sliders are everything the agent can ask for. Describe a tower you'd like in one sentence, then build it here. **Which of your words had no slider?**

<!-- notes -->
**The idea.** The same ideas as the add tool and the dice, now with a tool that's worth designing with. Eight **parameters** go in: floors, floor height, width, depth, twist, taper, lean and the direction of the lean. Out comes the geometry, an image and a list of **metrics**: height, floor area, footprint, top floor, slenderness, cantilever and shadow.

The plan view updates live as you drag the sliders. **Build with the tool** runs the full tool. **Build the same again** shows that, unlike a die, it gives exactly the same answer every time. That's what makes it fit for measuring.

**Limits** like `height_m>60` are checks the tool runs for you: each one passes or fails.

**Why it matters.** The agent can only *say* a design through these eight numbers, and only *judge* it through these metrics. Views, cost, how it feels at street level, whether it's memorable: if no metric captures it, the system can't notice it. Deciding what to measure is a design decision, and Session 2 starts there.

**Try it yourself.** In class you described a tower in one sentence and looked for sliders to match. Do it again with a different sentence, and keep a list of the words that had no slider and no metric. Bring the list to Session 2: it's where new measures come from.
