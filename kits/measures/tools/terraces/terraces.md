# Terraces: the open roof a tower leaves where a floor steps back

## Who asks, and why
Anyone who wants outdoor space up the tower: gardens, balconies, a terrace to sit on. A tower whose floors step back, shift or turn leaves part of each floor's roof open. This measures how much, and how big the largest single piece is.

## Inputs

| On the canvas | Unit | Allowed values | Default | Meaning |
|---|---|---|---|---|
| `in:floors` | | curves, e.g. `layer:runs::tower::A-calm::floors` | none | The floor outlines: the `floors` layer of a tower run |

## What it does
1. Sorts the floor outlines from bottom to top, by height.
2. For each floor except the top one: its outline minus the outline of the floor above, on that floor's level. What's left is open roof: a terrace.
3. Adds up the terrace areas, and finds the largest single piece.

The top floor's roof isn't counted: every tower has one.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:terrace_m2` | m² | All the terraces added up |
| `out:largest_terrace_m2` | m² | The biggest single piece of terrace |
| `out:terraces` | | The terraces as surfaces, baked to `runs::terraces::<run>::terraces` |

## Test cases
The towers are `tower.gh` runs, with everything else at its default (a 20 × 20 m floor).

| Inputs | Expected output |
|---|---|
| 12 floors, nothing else changed | `terrace_m2 = 0`, `largest_terrace_m2 = 0` (and a warning that no surfaces were made) |
| 30 floors, `taper = 0.5` | `terrace_m2 = 300` (400 m² ground floor − 100 m² top floor), `largest_terrace_m2 = 13.67` |
| 30 floors, `lean = 20, lean_dir = 180` | `terrace_m2 = 400` (29 strips of 20 × 0.69 m), `largest_terrace_m2 = 13.79` |
| 30 floors, `twist = 90` | `terrace_m2 = 297.66`, `largest_terrace_m2 = 2.57` (116 thin corner pieces) |

## What it can't tell you
Whether a terrace is usable, because it doesn't measure **depth**. The tapering tower above leaves 300 m² as rings 17 cm deep; the twisting one leaves 298 m² as corner slivers. `largest_terrace_m2` tells those two apart, but a 13.67 m² ring 17 cm deep is no more usable than a sliver. Look at the baked terraces. A strong lean leaves usable strips: 40 m over 20 floors shifts each floor 2.1 m. It also can't tell you about railings, structure, wind, or which way a terrace faces.

## Use it in a skill
A row for the Measures table in your `tower-in-rhino` skill:

`| tools/terraces/terraces.gh | floors = the tower run's floors layer | largest_terrace_m2 >= 20 |`
