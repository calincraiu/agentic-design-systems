# Later sessions: notes for building them

Nothing here is planned in detail yet.

- **Session 2 is built** (`slides/session-2/`, `instructor/session-2.md`): Grasshopper definitions as tools through one runner, the tower on a real site, a challenge on one measure (`park_sun`), Goodhart, and students choosing a second measure with their own limit. Kits: `gh`, `site`, `measures`. The Grasshopper bridge at `gh-bridge-v0` was not used: the runner replaced it.
- **Session 3 seeds from Session 2:** the take-home is a *contract* for a measure that isn't on the menu (structure, cost, street-level feel, terrace depth). Building some of those is a natural start: students know the convention (`in:`/`out:`, contract beside the `.gh`) and have built `floor_area`. `terraces` has a known blind side worth fixing: it doesn't measure depth, so a 17 cm ring counts as terrace.
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
