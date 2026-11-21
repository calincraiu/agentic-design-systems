<!-- layout: task | where: code-yours | time: 25 min | pairs -->
<p class="kicker">Part 2 · Measure · the challenge</p>

# The most floor area the park can take

**Rules:** the most floor area · the park loses **less than 20%** of its sun (`park_sun`, London) · the tower stays **inside the plot** (`beyond_plot_m = 0`).

1. **Agree** a strategy in one sentence.
2. **New session:** give `/tower-in-rhino` the rules instead of a wish.
3. **Check** the receipts of your best tower.
4. **Call out** its floor area, sun lost and beyond-plot.

> **You're done when** your best tower is on the scoreboard, with receipts to back it up.

<!-- notes -->
This is a design brief with only numbers in it. Floor area pulls one way and the park's sun pulls the other. Which part of a tower costs the park its sun (the footprint, the height, the shape) is for you and your agent to find out: run a few towers that differ in one thing only, and compare.

Give the agent the rules as they are written here. Your stance stays in the skill, so two pairs with different stances get different strategies from the same rules.

The numbers on the scoreboard must come from the receipts in `runs/`: `gfa_m2` and `beyond_plot_m` from the tower's receipt, and `sun_lost_percent` from `park_sun`'s receipt for the same label. A number that appears only in Claude's summary isn't on the scoreboard.

Each `park_sun` run takes about a second, so a full round of three variants and their measures takes under a minute of computing. Most of the time goes into Claude reading, deciding and reporting.
