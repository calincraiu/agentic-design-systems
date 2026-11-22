# Sum: adds two numbers in Grasshopper

## Who asks, and why
Anyone who wants two numbers added exactly. It is the Grasshopper version of Session 1's add tool, and the smallest possible Grasshopper tool. In class you build your own; this copy is the reference, if yours won't run.

## Inputs

| On the canvas | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `in:a` | any | 0 to 1000, two decimal places | 1 | The first number |
| `in:b` | same as `a` | 0 to 1000, two decimal places | 2 | The second number |

## What it does
1. Adds `a` and `b` with Grasshopper's Addition component.

## Outputs

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:sum` | same as the inputs | a + b |

## Test cases

| Inputs | Expected output |
|---|---|
| `a = 12.5, b = 30` | `sum = 42.5` |
| `a = 0.1, b = 0.2` | `sum = 0.3` |
| `a = 2000, b = 1` | refused: 2000 is outside 0 to 1000 |
| `a = 0.125, b = 1` | refused: more than two decimal places |

## What it can't tell you
Whether the two numbers are in the same unit. Adding 3 m to 250 mm gives 253, and the tool won't notice.
