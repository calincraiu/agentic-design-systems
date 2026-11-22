<!-- layout: diagram | where: app -->
<p class="kicker">Part 2 · A chain on the site</p>

# The wish, on a real site

<div data-widget="figure" data-name="site" data-ghost></div>

> *"A tower on a 30 × 30 m plot next to a park: calm, but noticed from the river."*

<!-- notes -->
This is the wish you gave Chat at the start of Session 1. The tower tool then had no idea where the park or the river was: its shadow metric measured all the ground in shadow, at one sun angle, wherever that ground was.

The plan is drawn to scale, north up. The plot is 30 × 30 m. A 12 m street separates it from the park to the north, which measures 90 × 60 m, so in the northern hemisphere the tower's shadow falls towards the park. Beyond the park runs a river 40 m wide, with seven viewpoints along its middle at eye height (1.6 m). Five neighbouring blocks, 15 to 24 m high, stand around the plot and on either side of the park.

The same site is in the `site` kit as `site/site.3dm`, in metres, with one layer for each part: `Site::Plot`, `Site::Park`, `Site::River`, `Site::River views` and `Site::Neighbours`. Tools find their geometry by these layer names.
