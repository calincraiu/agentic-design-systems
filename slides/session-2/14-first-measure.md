<!-- layout: task | where: code-yours | time: 5 min -->
<p class="kicker">Part 2 · Measure · your turn</p>

# Add your first measure

1. **Take** the `measures` kit (below).
2. **Read** `tools/park_sun/park_sun.md`, especially *What it can't tell you*.
3. **Paste** its *Use it in a skill* row into the **Measures** table of your `tower-in-rhino` skill, in place of *(none yet)*.

<div data-widget="takeaway" data-kit="measures"></div>

> **You're done when** your Measures table has one row, ending `sun_lost_percent < 20`.

<!-- notes -->
`park_sun` measures the direct sun on the park on 21 March, every 15 minutes, on points 2 m apart, using Ladybug. It runs twice: once with the tower and the neighbours casting shadows, and once with the plot left empty. **Sun lost** is the difference as a share of the empty-plot sunshine. A 12-floor tower on the site takes 12.6% of the park's sun in London; a 40-floor one, 18.8%.

The limit comes from a real guide. The UK's BRE guide *Site layout planning for daylight and sunlight* (BR 209) treats an open space that keeps less than 0.8 times its former sunlight, a loss of more than 20%, as noticeably affected. The tool applies that idea to the park's average sun hours.

The city is an input, chosen from a dropdown inside the definition, with London as the default. Ladybug can't look a place up by name, so each city in the list carries its own latitude, longitude and time zone. To add one, add a line to the dropdown in `park_sun.gh`.

From now on, `/tower-in-rhino` runs every measure in its table on every variant, checks the limits, and gives a failing variant one revision at most.
