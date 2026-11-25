# River view: how much of the tower people on the river see

## Who asks, and why
Anyone who wants a tower to be "noticed from the river", or, the other way round, to stay out of the river's view. Seeing is two-way: the parts of the tower seen from the river are also the parts that look out at it. It uses Ladybug.

## Inputs

| On the canvas | Unit | Allowed values | Default | Meaning |
|---|---|---|---|---|
| `in:tower` | | geometry, e.g. `layer:runs::tower::A-calm::mass` | none | The tower: the `mass` layer of a tower run |
| `in:context` | | geometry, e.g. `layer:Site::Neighbours` | none | Buildings that block the view |
| `in:viewpoints` | | points, e.g. `layer:Site::River views` | none | Where people look from: 7 points on the river at eye height |

## What it does
1. Puts points 2 m apart on the tower's surface.
2. For each point, finds the share of viewpoints that can see it, with the neighbours and the tower itself in the way (Ladybug's Visibility Percent).
3. Seen area = that share, averaged over the tower's surface, × the surface area. It is the area of tower an average person on the river sees.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:seen_m2` | m² | Area of the tower seen from the river, averaged over the viewpoints |
| `out:view_map` | | The tower coloured by how many viewpoints see each part, baked to `runs::river_view::<run>::view_map` |

## Test cases
On `site/site.3dm`, with `context = layer:Site::Neighbours` and `viewpoints = layer:Site::River views`. The towers are `tower.gh` runs (20 × 20 m floors unless changed).

| Inputs | Expected output |
|---|---|
| 12 floors | `seen_m2 = 1315.57` |
| 30 floors, `taper = 0.5` | `seen_m2 = 2970.96` |
| 30 floors, `lean = 20, lean_dir = 180` | `seen_m2 = 3828.06` |
| 30 floors, `twist = 90` | `seen_m2 = 4081.73` |

## What it can't tell you
Whether people notice what they see: a plain slab and a landmark can show the same area. Distance, haze and trees: every viewpoint counts the same, near or far. Views from anywhere other than the 7 river points.

## Use it in a skill
A row for the Measures table in your `tower-check` skill. The limit is only a starting point: change it to one you can defend, and write why in the last cell.

`| tools/river_view/river_view.gh | tower = the tower run's mass layer, context = layer:Site::Neighbours, viewpoints = layer:Site::River views | seen_m2 >= 3000 | (your reason) |`
