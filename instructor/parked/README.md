# Parked slides: your own tool

These two slides were the end of Session 1. Session 2 didn't use them: its tool task is a Grasshopper one (`floor_area`, slide 11), with the same contract idea in `kits/gh/tools/grasshopper/TEMPLATE.md`. They stay here as an optional exercise (a Python tool written by `/tool-builder` from a contract), outside `slides/`, so the app doesn't show them.

- `36-your-own-tool.md`: the section slide (uses the `contract` figure)
- `37-own-tool.md`: the task (uses the `tool-spec` kit and `kits/tool-spec/tools/stair_check.md`)

## Teaching it

The point is that **authoring a tool means authoring its contract**: inputs, ranges, the rule in words, the output, and test cases worked out by hand. Students don't need to read the code: `/tool-builder` writes it, then runs *their* test cases. Its most useful moment is step 2, when it questions the contract before writing anything: unclear rounding, a missing unit, a test case the rule doesn't produce.

Good sizes: stair fit (the worked example), brick coursing, ramp gradient, parking count, room-area schedule. Too big: anything needing geometry, images or the internet.
