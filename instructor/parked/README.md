# Parked slides: your own tool

These two slides were the end of Session 1. They now open **Session 2**, where writing a tool's contract leads straight into *Tool* and *Measure* on the ladder. They live here, outside `slides/`, so the app doesn't show them and they aren't in the student zip.

- `36-your-own-tool.md`: the section slide (uses the `contract` figure)
- `37-own-tool.md`: the task (uses the `tool-spec` kit and `kits/tool-spec/tools/stair_check.md`)

When Session 2's deck exists, move them into `slides/session-2/` and renumber. The figure and the kit are still in place.

## Teaching it

The point is that **authoring a tool means authoring its contract**: inputs, ranges, the rule in words, the output, and test cases worked out by hand. Students don't need to read the code: `/tool-builder` writes it, then runs *their* test cases. Its most useful moment is step 2, when it questions the contract before writing anything: unclear rounding, a missing unit, a test case the rule doesn't produce.

Good sizes: stair fit (the worked example), brick coursing, ramp gradient, parking count, room-area schedule. Too big: anything needing geometry, images or the internet.
