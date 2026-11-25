# Park sun: how much of the park's sunshine the tower takes away

## Who asks, and why
Anyone who promised that a tower would be kind to the park next to it. It measures the sun on the park on one day, 21 March, with and without the tower, in a city you choose. It uses Ladybug.

## Inputs

| On the canvas | Unit | Allowed values | Default | Meaning |
|---|---|---|---|---|
| `in:tower` | | geometry, e.g. `layer:runs::tower::A-calm::mass` | none | The tower: the `mass` layer of a tower run |
| `in:context` | | geometry, e.g. `layer:Site::Neighbours` | none | Other buildings that also cast shadows |
| `in:park` | | geometry, e.g. `layer:Site::Park` | none | The ground to measure |
| `in:city` | | a city in the dropdown: London, Paris, Berlin, Copenhagen, Rotterdam, Vienna, Milan, Barcelona, Bucharest, Athens, New York, Singapore, Sydney | London | Where the site is. To add a city, add a line to the dropdown: `name;latitude;longitude;time zone` |

## What it does
1. Looks up the city's latitude, longitude and time zone in the dropdown.
2. Finds the sun's position every 15 minutes on 21 March (Ladybug's sun path).
3. Puts points 2 m apart on the park and counts, for each point, the hours the sun reaches it, with the tower and the neighbours in the way. Averages them.
4. Does the same with the neighbours only: the plot left empty.
5. Sun lost = (empty plot − with tower) ÷ empty plot × 100.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:sun_hours` | h | Average hours of direct sun on the park, with the tower |
| `out:sun_hours_empty_plot` | h | The same with the plot left empty |
| `out:sun_lost_percent` | % | How much of the park's sun the tower takes away |
| `out:sun_map` | | A coloured map of sun hours on the park, baked to `runs::park_sun::<run>::sun_map` |
| `out:location` | | The location it used, to check the city |

The UK's BRE guide on daylight and sunlight (BR 209) treats keeping less than 0.8 times the former sunlight, a loss of more than 20%, as noticeable. This tool applies that idea to the average sun hours on the park.

## Test cases
On `site/site.3dm`, with `park = layer:Site::Park` and `context = layer:Site::Neighbours`. The towers are `tower.gh` with only `floors` changed.

| Inputs | Expected output |
|---|---|
| no tower, `city = London` | `sun_hours = 7.45` (and a warning that `in:tower` is empty) |
| 12-floor tower, `city = London` | `sun_hours = 6.51`, `sun_hours_empty_plot = 7.45`, `sun_lost_percent = 12.58` |
| 40-floor tower, `city = London` | `sun_hours = 6.05`, `sun_lost_percent = 18.79` |
| 30 floors, `taper = 0.5`, `city = London` | `sun_lost_percent = 15.4` |
| 30 floors, `twist = 90`, `city = London` | `sun_lost_percent = 19.02` |
| 30 floors, `lean = 20, lean_dir = 180`, `city = London` | `sun_lost_percent = 16.6` |
| 40-floor tower, `city = Bucharest` | `sun_hours_empty_plot = 8.02`, `sun_lost_percent = 16.34` |
| 40-floor tower, `city = Sydney` | `sun_lost_percent = 0`: the shadow falls south, away from the park |
| `city = Cluj` | refused: not in the dropdown |

## What it can't tell you
Any other day: winter shadows are much longer, summer ones much shorter. Whether the sun lands where people sit, play or grow things. Sunlight on the neighbours' windows (that's `neighbours_sun`). The feeling of a tall building standing over a park, which has nothing to do with sun hours.

## Use it in a skill
A row for the Measures table in your `tower-check` skill. The limit is only a starting point: change it to one you can defend, and write why in the last cell.

`| tools/park_sun/park_sun.gh | tower = the tower run's mass layer, park = layer:Site::Park, context = layer:Site::Neighbours, city = London | sun_lost_percent < 20 | (your reason) |`
