<!-- layout: stage | where: app -->
<p class="kicker">Part 2 · A tower</p>

# Eight numbers in, a measured tower out

<div data-widget="tower" data-plot="30x30" data-require="height_m>60"></div>

> These sliders are everything the agent can ask for. Describe a tower you'd like in one sentence, then build it here. **Which of your words had no slider?**

<!-- notes -->
The tower tool works like the add tool, with more inputs. Eight **parameters** go in: floors, floor height, width, depth, twist, taper, lean and the direction of the lean. Out come the geometry, an image and a set of **metrics**: height, floors, floor area, footprint, top floor area, how far it reaches past the plot, slenderness, cantilever and shadow.

The shadow figure is rough. It is the total ground area in shadow with the sun due south at 35° above the horizon, which assumes a northern-hemisphere site. The tool draws one outline around all the shadow points, so it overestimates. And it doesn't know where the park is, so it can't say how much of that shadow falls on it.

The plan view updates as you drag the sliders. **Build with the tool** runs the full tool. **Build the same again** shows that, unlike the dice, it returns identical results for identical inputs. **Limits** such as `height_m>60` are checks the tool runs on each result, and each one passes or fails.

The agent can only describe a design through these eight numbers, and only judge it through these metrics. Views, cost, how it feels at street level and whether it's memorable aren't measured, so the system can't take them into account. Choosing what to measure is a design decision, and it is where Session 2 starts.

Describe a different tower in one sentence and try to set it with the sliders. List the words that had no slider and no metric.
