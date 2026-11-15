# Later sessions: notes for building them

Nothing here is planned in detail yet.

- **Session 2:** students create a tool and write their own measures. The structured JSON brief may come back here, once it has a reason to exist.
- **Session 3:** Grasshopper. The tower becomes "same tool, new engine".
- Each session adds a slide deck (`slides/session-2/`) and, if needed, a new kit. Students get a fresh course-folder zip, and their own folder is never touched. A new kit must never contain a file with the same path as something students have written.
- Session 2 builds on the own-tool contract from Session 1: add a measure to the tower, or write a tool that measures something the tower can't (terraces, for example: the first thing students usually ask for that no metric measures).

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
