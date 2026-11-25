<!-- layout: section | where: app -->
<p class="kicker">Part 2 · A chain on the site</p>

# Same runner, a tower

<p class="lead">One tool's output is the next tool's input.</p>

<div data-widget="figure" data-name="chain" data-start="3" data-ghost class="map"></div>

<!-- notes -->
The tower from Session 1 has been rebuilt in Grasshopper, and the runner runs it exactly as it ran your sum. The difference is that the tower is geometry: the runner bakes it into Rhino on a layer of its own, and other tools can read that layer. A **measure** is one of those: a tool that takes a design and returns a number about it, such as the share of the park's sunshine the tower takes away. Chaining tools this way, through layers and numbers, is how small tools add up to a design workflow.
