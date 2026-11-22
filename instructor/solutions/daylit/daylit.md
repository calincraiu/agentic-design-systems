# Daylit: how much of a tower's floor area is near a window

<!-- The instructor's reference for slide 13. Students write their own contract first, then build the
     definition by hand. Built by scripts/make_gh.py (make_daylit); checked in Rhino 9 through the runner. -->

## Who asks, and why
Anyone planning floors that people work or live on. Daylight from a side window only reaches so far into a room. A deep floor plate gives more floor area, but its middle needs electric light all day. This tells you how much of the tower is within reach of a window.

## Inputs

| On the canvas | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `in:floors` | | curves, e.g. `layer:runs::tower::A-calm::floors` | none | The floor outlines: the `floors` layer of a tower run |
| `in:depth` | m | 3 to 12, 1 decimal | 7 | How far daylight reaches in from the façade. 7 m is about 2.5 × a window head 2.8 m above the floor |

## What it does
1. Offsets each floor outline inward by `depth`. What is left inside is that floor's dark core. A floor narrower than 2 × `depth` has no core: Grasshopper says "Curve offset failed" for it, and its dark area is 0.
2. Adds up the dark cores' areas: `dark_m2`.
3. Adds up the floor outlines' areas: the floor area.
4. Daylit share = 100 × (1 − dark area ÷ floor area).

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:daylit_percent` | % | The share of the floor area within `depth` of the façade |
| `out:dark_m2` | m² | The floor area further than `depth` from the façade, all floors together |

## Test cases
The towers are `tower.gh` with only the inputs shown changed (12 floors unless stated).

| Inputs | Expected output |
|---|---|
| 20 × 20 m tower, `depth = 7` | `daylit_percent = 91` (a 6 × 6 m core on each floor: `dark_m2 = 432`) |
| 30 × 30 m tower, `depth = 7` | `daylit_percent = 71.56` (a 16 × 16 m core: `dark_m2 = 3072`) |
| 12 × 12 m tower, `depth = 7` | `daylit_percent = 100`, `dark_m2 = 0`, and "Curve offset failed" (no floor has a core) |
| 20 × 20 m tower, `depth = 5` | `daylit_percent = 75` |
| 30 floors, `twist = 90`, `depth = 7` | `daylit_percent = 91`: turning a floor doesn't change how deep it is |
| `depth = 13` | refused: outside 3 to 12 |

## What it can't tell you
Where the windows are, how big they are, or what is outside them: it treats the whole outline as glass with open sky beyond. The neighbours' shadow, the orientation, and whether the core is where you wanted the lifts and stairs anyway. A dark core is not always a problem.

## Use it in a skill
A row for the Measures table in your `tower-check` skill:

`| tools/daylit/daylit.gh | floors = the tower run's floors layer, depth = 7 | daylit_percent >= 85 | (your reason) |`
