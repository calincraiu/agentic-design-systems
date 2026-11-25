<!-- layout: task | where: code-yours | time: 25 min -->
<p class="kicker">Part 2 · A chain on the site · your turn</p>

# Put a tower on the site, and measure it

1. **Take** the `site` and `measures` kits (below).
2. In Rhino, **File › Open** `site/site.3dm` from your folder.
3. **New session:** ask for a tower in plain words, e.g. *"Put a 30-floor tower on the site, twisted by 45°."* Then ask for 100 floors.
4. **Pick** one measure from the `measures` kit: `park_sun`, `neighbours_sun`, `river_view` or `terraces`. **Read** its contract, then **ask** Claude to run it on your tower, e.g. *"How much of the park's sun does that tower take?"*
5. **Open** both receipts, then find the `in:` and `out:` names in `tools/tower/tower.gh`.

<div data-widget="takeaway" data-kit="site,measures"></div>

> **You're done when** a tower stands on the site, 100 floors was refused, and you have a tower receipt and a receipt from the measure you picked, with the same label.

<!-- notes -->
#### What you're building
A tower on the real site, built by the tower tool, then measured by a second tool: a measure someone else built, which you choose from four. The tower's layer is the link between the two. In the next task you build a measure yourself.

#### Steps
1. **Take** the `site` and `measures` kits with the prompt on the slide.
2. **Open** `site/site.3dm` in Rhino with File › Open. *Not Import: importing into a millimetre file scales the site, and every tool then warns about units.*
3. **Start** a new session and ask for a tower in plain words, e.g. *"Put a 30-floor tower on the site, twisted by 45°."* It appears on the site.
4. **Ask** for 100 floors. *Refused: the floors slider in `tower.gh` stops at 80.*
5. **Pick** a measure and open its contract in `tools/<measure>/<measure>.md`. *The contract says what it asks and what it can't tell you.* Then ask for it in plain words, e.g. *"How much of the park's sun does that tower take?"* Claude reads the contract and gives the measure the tower's layer, `layer:runs::tower::<run>::mass`. Try a second measure if you have time.
   - "No module named ladybug…" (`park_sun`, `neighbours_sun`): pick `river_view` or `terraces`, or pair up.
6. **Open** both receipts in `runs/`: the tower's and the measure's, with the same label.
7. **Open** `tools/tower/tower.gh` in Grasshopper and find the `in:` and `out:` names.

#### Background
The `site` kit has the site file, the tower as a Grasshopper tool (`tools/tower/tower.gh`, with its contract `tower.md`), and two skills for Part 3. The `measures` kit has four measures, each a Grasshopper tool with its contract. The other three are `neighbours_sun`, `river_view` and `terraces`; their contracts say what each one asks.

The tower is the same tool as `tower.py`, with the same eight numbers: the same inputs give the same floor area (to within 0.01 m²) and height. It also reports `beyond_plot_m`: how far any floor reaches past the plot, seen from above.

Each run bakes its tower to layers such as `runs::tower::A::mass` (one block per floor) and `runs::tower::A::floors` (the floor outlines), and hides earlier runs. Switch them back on in Rhino's Layers panel to compare.

`park_sun` uses Ladybug to count the hours of direct sun on points 2 m apart across the park on 21 March, with the tower and without it. **Sun lost** is the difference as a share of the sun without it. A 12-floor tower takes 12.6% of the park's sun in London, a 40-floor one 18.8%. Each run takes about a second.
