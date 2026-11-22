# Later sessions: notes for building them

Nothing here is planned in detail yet.

- **Session 2 is built** (`slides/session-2/`, `instructor/session-2.md`), reworked on 2026-11-22 into one chain built link by link. Students build `sum.gh` by hand (the first Grasshopper tool, and the in-class setup check). The same runner then drives the tower on the real site and `park_sun` on its layer. Students build a measure, `daylit`, and write `tower-check`, a skill with their measures and limits, which `tower-in-rhino` uses to judge its variants. Kits: `gh`, `site`, `measures`, and `sum` (the reference copy). The challenge, scoreboard and Goodhart were dropped (see below). The Grasshopper bridge at `gh-bridge-v0` was not used: the runner replaced it.
- **Session 3 seeds from Session 2:** the take-home is a *contract* for a tool from the student's own studio project, with one line on which skill would run it and what it would feed. Building some of those, and wiring several together, is the natural next step towards the **workflow** rung of the ladder: students know the convention (`in:`/`out:`, a contract beside the `.gh`, a row for a skill) and have built `sum` and `daylit`. `terraces` has a known blind side worth fixing: it doesn't measure depth, so a 17 cm ring counts as terrace.
- **Tool Exchange** (parked idea): pairs swap measures, and the other pair's agent must use one from its contract alone.
- **The tower tool's linear taper** can't make stepped setbacks, so real terraces only come from leaning. Wanting setbacks is a reason to change the *tool* (a new `tower.gh` parameter), which suits a "change the engine" exercise.
- Each session adds a slide deck and, if needed, a new kit. Students get a fresh course-folder zip, and their own folder is never touched. A new kit must never contain a file with the same path as something students have written.

## Getting the Grasshopper bridge back

The bridge is preserved at the git tag `gh-bridge-v0`. To see what's there:

```
git ls-tree -r --name-only gh-bridge-v0 kit examples
```

To restore the Grasshopper parts into the working folder:

```
git checkout gh-bridge-v0 -- kit/gh kit/bridge.py examples/tower/GH_SPEC.md examples/tower/unpack.py tests/fake_gh.py tests/test_bridge.py tests/test_gh_scripts.py
```

They won't run as they are. They import from `kit.paths`, which no longer exists, and `kits/tower/tools/tower/tower.py` needs its `--backend` flag back (see `examples/tower/cli.py` at the tag for how it worked). The bridge writes `geometry.json` in the format the tower tool still uses (`curves`, `floor_height`), and `evaluate()` only reads that, so measuring works unchanged.

**Still untested from the first version:** the Grasshopper scripts have only been run against a fake Grasshopper, never in real Rhino 7 or 8. `tower.gh` was never assembled.

## Goodhart, parked from Session 2

Session 2 had a challenge: pairs had `/tower-in-rhino` find "the most floor area while the park loses less than 20% of its sun and the tower stays inside the plot", with a scoreboard, then looked at the winner against the wish ("When a measure becomes a target, it ceases to be a good measure": Marilyn Strathern, 1997, after Charles Goodhart). It was dropped as too much for that stage, and as gamification that made the flow clunky. If it comes back (it suits a session where students have several measures to trade off), these are the numbers, measured with the kits (Rhino 9, London, the site as built):

- **Height is free above about 20 floors.** On 21 March the sun in London is low (about 38° at noon), so a tower's shadow already reaches past the park by about 70 m of height. A 20 × 20 m tower loses 7.2% of the park's sun at 8 floors, 12.6% at 12, 18.7% at 20, and 18.79% at 24, 40, 60 and 80 floors alike.
- **The footprint decides.** At any height above that: 20 × 20 m 18.8%, 21 × 21 m 19.75% (passes), 22 × 22 m 20.7% (fails). Orientation matters too: 14 m east-west × 30 m north-south loses 18.1%, the same footprint turned the other way 23.2%.
- **The best tower found:** 80 floors (the slider's maximum, 280 m) on an 18 × 18 m base that widens upward to 30 m (`taper = 1.66`): 46,815 m², 18.4% sun lost, inside the plot. A straight 21 × 21 m × 80 floors gives 35,280 m². The widest box that passes, 30 × 30 m, only manages 11 floors (9,900 m², 19.0%).
- **Leaning south**, away from the park, quickly leaves the plot (`beyond_plot_m`): a 20 m lean over 30 floors is 15 m out. The plot rule is what stops that exploit.
- **Twisting** changes little for the park; it raises `river_view` and leaves sliver terraces (`terraces`: 298 m² in pieces of at most 2.6 m²).
- The old scoreboard widget is in git history (`app/static/app.js`, before 2026-11-22), and so are the old slides 14–17.
