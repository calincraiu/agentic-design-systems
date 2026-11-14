# Stair check: does a straight stair fit, and is it comfortable?

## Who asks, and why
An architect fitting a straight flight between two floors, who wants to know quickly whether the space they have makes a comfortable stair.

## Inputs

| Name | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `--floor-height` | m | 2 to 6 | (required) | Finished floor to finished floor |
| `--run` | m | more than 0, up to 20 | (required) | Horizontal length available for the flight |
| `--max-riser` | mm | 120 to 220 | 175 | Highest step allowed |
| `--min-going` | mm | 200 to 350 | 250 | Shallowest tread allowed |

The defaults are this example's assumptions, not a building code. Check the rules where you build.

## What it does
1. Number of risers = floor height ÷ max riser, **rounded up** to a whole number.
2. Riser height = floor height ÷ number of risers.
3. Number of treads = number of risers − 1 (the top floor is the last step).
4. Going = run ÷ number of treads.
5. Blondel's rule: 2 × riser + going should be between 600 and 650 mm, the length of a comfortable step.
6. Pitch = the angle whose tangent is riser ÷ going.
7. Check: riser ≤ max riser, going ≥ min going, 600 ≤ 2R+G ≤ 650.

## Output
```
Risers: 18 x 166.7 mm
Treads: 17 x 264.7 mm
Pitch: 32.2 deg
Blondel 2R+G: 598.0 mm
PASS  riser 166.7 <= 175 mm
PASS  going 264.7 >= 250 mm
FAIL  Blondel 598.0 between 600 and 650 mm
```
Lengths to one decimal place. One line per check: PASS or FAIL, then the rule it checked.

## It refuses when
- Floor height is outside 2 to 6 m, or run is 0 or less.
- Max riser or min going is outside its range.

## Test cases

| Inputs | Expected output |
|---|---|
| `--floor-height 3 --run 4.5` | 18 risers of 166.7 mm, 17 treads of 264.7 mm, 2R+G 598.0: riser PASS, going PASS, **Blondel FAIL** |
| `--floor-height 3 --run 4.8` | 18 risers of 166.7 mm, 17 treads of 282.4 mm, 2R+G 615.7: **all PASS**, pitch 30.6 deg |
| `--floor-height 2.8 --run 3` | 16 risers of 175.0 mm, 15 treads of 200.0 mm: riser PASS, **going FAIL**, **Blondel FAIL** (550.0) |
| `--floor-height 9 --run 4` | refuses: floor height outside 2 to 6 m |

## What it can't tell you
Headroom, landings, winders, handrails, width, or whether the stair suits the building. It checks one straight flight.
