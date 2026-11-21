# Tower: Session 1's tower, built in Grasshopper on the real site

## Who asks, and why
Anyone exploring a tower for the 30 × 30 m plot in `site/site.3dm`. It takes the same eight numbers as `tower.py` and builds the same tower, but in Rhino, next to the park and the river, where other tools can measure it.

## Inputs

| On the canvas | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `in:floors` | | 1 to 80, whole | 12 | Number of storeys |
| `in:floor_height` | m | 2.8 to 6, 2 decimals | 3.5 | Floor-to-floor height |
| `in:width` | m | 6 to 60, 1 decimal | 20 | Ground floor size east-west |
| `in:depth` | m | 6 to 60, 1 decimal | 20 | Ground floor size north-south |
| `in:twist` | deg | −360 to 360, whole | 0 | Rotation from the ground floor to the top floor (positive = anticlockwise from above) |
| `in:taper` | × | 0.2 to 2, 2 decimals | 1 | Top floor size relative to the ground floor |
| `in:lean` | m | 0 to 40, 1 decimal | 0 | How far the top floor is shifted sideways |
| `in:lean_dir` | deg | 0 to 360, whole | 0 | Compass direction of the lean (0 = north, 90 = east) |
| `in:plot` | | a closed curve, e.g. `layer:Site::Plot` | the site's 30 × 30 m plot | The plot boundary. Leave it out to use the site's plot |

## What it does
For each floor, *t* runs from 0 (ground floor) to 1 (top floor).

1. Draw a width × depth rectangle centred on the middle of the plot.
2. Scale it by 1 + (taper − 1) × *t*.
3. Turn it by twist × *t* degrees.
4. Shift it by lean × *t* towards `lean_dir`, and lift it to floor number × floor height.
5. Extrude each outline one floor height up: one block per floor.
6. Floor area = all the floor outlines' areas added up. Height = floors × floor height.
7. Beyond the plot: for every floor corner that lies outside the plot (seen from above), its distance to the plot's edge. The largest one; 0 if the whole tower stays inside.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:floors` | | The floor outlines, baked to `runs::tower::<run>::floors` |
| `out:mass` | | One block per floor, baked to `runs::tower::<run>::mass` |
| `out:gfa_m2` | m² | Gross floor area |
| `out:height_m` | m | Height to the roof |
| `out:beyond_plot_m` | m | How far any floor reaches beyond the plot, seen from above (0 = inside) |

## Test cases
The same inputs given to `tower.py` give the same results (floor areas within 0.01 m²: `tower.py` rounds its corners to 0.1 mm).

| Inputs | Expected output |
|---|---|
| none (all defaults) | `gfa_m2 = 4800`, `height_m = 42`, `beyond_plot_m = 0` |
| `floors = 30, floor_height = 3.2, width = 24, depth = 18, twist = 90, taper = 0.6, lean = 8, lean_dir = 45` | `gfa_m2 = 8479.12`, `height_m = 96` |
| `floors = 1, width = 10, depth = 12` | `gfa_m2 = 120`, `height_m = 3.5` |
| `floors = 40, width = 15.5, depth = 33.3, twist = -200, taper = 1.8, lean = 40, lean_dir = 200` | `gfa_m2 = 41623.75`, `height_m = 140`, `beyond_plot_m = 55.52` |
| `floors = 30, lean = 20, lean_dir = 180` | `beyond_plot_m = 15` (the top floor's south edge is 15 m past the plot) |
| `width = 34` | `beyond_plot_m = 2` (2 m over on each side) |
| `floors = 81` | refused: outside 1 to 80 |

## What it can't tell you
Anything about the park, the river or the neighbours: it builds the tower, it doesn't judge it. That's what measures are for. Whether reaching beyond the plot is allowed: it says how far, not whether that's acceptable over a street.
