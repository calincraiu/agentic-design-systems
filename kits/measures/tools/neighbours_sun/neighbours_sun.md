# Neighbours' sun: how much sunshine the tower takes from the buildings around it

## Who asks, and why
The people next door. A tower doesn't only shade the park: it shades the walls and roofs of the neighbouring blocks, where windows and solar panels are. It measures the sun on them on 21 March, with and without the tower. It uses Ladybug.

## Inputs

| On the canvas | Unit | Allowed values | Default | Meaning |
|---|---|---|---|---|
| `in:tower` | | geometry, e.g. `layer:runs::tower::A-calm::mass` | none | The tower: the `mass` layer of a tower run |
| `in:neighbours` | | geometry, e.g. `layer:Site::Neighbours` | none | The buildings to measure. They also shade each other |
| `in:city` | | a city in the dropdown (as in `park_sun`) | London | Where the site is |

## What it does
1. Finds the sun's position every 15 minutes on 21 March in that city.
2. Puts points 2 m apart on the neighbours' walls and roofs, and counts the hours of sun at each, with the tower in the way. Averages them.
3. Does the same without the tower.
4. Sun lost = (without − with) ÷ without × 100.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:sun_hours` | h | Average hours of sun on the neighbours, with the tower |
| `out:sun_hours_empty_plot` | h | The same without the tower |
| `out:sun_lost_percent` | % | How much of the neighbours' sun the tower takes away |
| `out:sun_map` | | A coloured map of sun hours on the neighbours, baked to `runs::neighbours_sun::<run>::sun_map` |
| `out:location` | | The location it used |

## Test cases
On `site/site.3dm`, with `neighbours = layer:Site::Neighbours` and `city = London`. The towers are `tower.gh` runs (20 × 20 m floors unless changed).

| Inputs | Expected output |
|---|---|
| 12 floors | `sun_hours = 5.57`, `sun_hours_empty_plot = 5.79`, `sun_lost_percent = 3.69` |
| 30 floors, `taper = 0.5` | `sun_lost_percent = 5.65` |
| 30 floors, `twist = 90` | `sun_lost_percent = 6.82` |
| 30 floors, `lean = 20, lean_dir = 180` | `sun_lost_percent = 7.95` |

## What it can't tell you
Which neighbour loses the sun: it averages all five blocks, so a big loss on one wall can hide behind four unaffected buildings (look at the sun map). Where the windows are. Any day other than 21 March.

## Use it in a skill
A row for the Measures table in your `tower-check` skill. The limit is only a starting point: change it to one you can defend, and write why in the last cell.

`| tools/neighbours_sun/neighbours_sun.gh | tower = the tower run's mass layer, neighbours = layer:Site::Neighbours, city = London | sun_lost_percent < 5 | (your reason) |`
