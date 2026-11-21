<!-- layout: task | where: code-yours | time: 25 min -->
<p class="kicker">Part 1 · Tool · your turn</p>

# Put the tower on its site

1. **Take** the `site` kit (below).
2. In Rhino, **File › Open** `site/site.3dm` from your folder.
3. **Paste** your Session 1 stance into *Design stance* in `.claude/skills/tower-in-rhino/SKILL.md`.
4. **New session:** run `/tower-in-rhino` with the Session 1 wish.

<div data-widget="takeaway" data-kit="site"></div>

> **You're done when** three towers have stood on the site, and you've read what the report says it judged by eye.

<!-- notes -->
The `site` kit has the site file, the tower as a Grasshopper tool (`tools/tower/tower.gh`, with its contract `tower.md`), and a new skill, `tower-in-rhino`. The skill works like `tower-designer`: it listens, asks three questions, writes a brief and builds three variants. The difference is that the towers now stand on the site in Rhino, and Claude looks at each one with a viewport picture.

**Open the site, don't import it.** The file is in metres. Importing it into a new Rhino file in millimetres scales everything to millimetres, and every tool then warns about units.

**The stance.** Your Session 1 stance is in your own `tower-<stance>` skill (or in `tower-designer`, if you edited it in place). Copy your three sentences over the *Balanced* paragraph in the new skill. The same stance now meets the real site.

Each run bakes its tower to a layer, such as `runs::tower::A-quiet-slab::mass`, and hides the earlier runs, so you always see the newest one. The earlier ones are still there: switch their layers back on in Rhino's Layers panel to compare.

The tower is the same tool as `tower.py`, rebuilt in Grasshopper from the same steps. Give both the same eight numbers and you get the same floor area (to within 0.01 m²) and height; its contract lists the test cases that show it. It also reports `beyond_plot_m`: how far any floor reaches past the plot, seen from above.

Look at the last part of the report. With no measures yet, the skill can only judge the shadow on the park or the view from the river **by eye**, and it has to say so. That gap is where Part 2 starts.
