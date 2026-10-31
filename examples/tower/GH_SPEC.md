# Building `tower.gh`

This is the wiring spec for the Grasshopper version of the Tower Toy. Build it once, save it as `examples/tower/tower.gh` **inside the repo** (the Listener finds the repo by looking for `pyproject.toml` above the .gh file), and it will drive and answer the agent's jobs.

The tower in this file must match the Python generator in [generate.py](generate.py). `tower generate` warns if the floor areas differ by more than 1%, which makes a handy check while you build.

Build it in **Rhino 7** with *GhPython Script* components. The file opens in Rhino 8 on Windows and Mac. If the legacy components misbehave there, paste the same code into Rhino 8 *Python 3 Script* components; it is written to run in both.

## Overview

```
[Agent control]──┐
[Panel "tower"]──┼─► LISTENER ──job──► UNPACK ◄── 8 sliders
                 │       │                │
                 │    status            8 values
                 │       ▼                ▼
                 │    [Panel]        TOWER GEOMETRY (native components)
                 │                        │ floor outlines
                 └──────job──────────────►WRITER ◄── keys "floor_height" / values
                                           │
                                        status ► [Panel]
```

Put the parts in three named groups: **1 Bridge in**, **2 Tower**, **3 Bridge out**. Students will read this canvas.

## 1 · Bridge in

| Component | Where | Settings |
|---|---|---|
| Boolean Toggle | Params › Input | Nickname **Agent control**, set to True |
| Panel | Params › Input | Text: `tower` |
| **Listener** (GhPython Script) | Maths › Script | Paste [kit/gh/listener.py](../../kit/gh/listener.py). Inputs (Item access, type hints): `active` bool, `system` str, `interval` int (leave unconnected = 500 ms). Outputs: `job`, `status` |
| Panel × 2 | | One on `status`, one on `job` (showing the job's JSON on the canvas is part of the teaching) |
| 8 × Number Slider | Params › Input | See the table below |
| **Unpack** (GhPython Script) | Maths › Script | Paste [unpack.py](unpack.py). Inputs (Item access): `job` str, then `slider_floors` int and `slider_floor_height`, `slider_width`, `slider_depth`, `slider_twist`, `slider_taper`, `slider_lean`, `slider_lean_dir` as float. Outputs: `floors`, `floor_height`, `width`, `depth`, `twist`, `taper`, `lean`, `lean_dir`, `source` |

Sliders (name each slider after its parameter, so it is obvious which Unpack input it feeds):

| Slider | Type | Min | Max | Default |
|---|---|---|---|---|
| floors | Integer | 1 | 80 | 12 |
| floor_height | Float, 2 dp | 2.8 | 6.0 | 3.5 |
| width | Float, 1 dp | 6 | 60 | 20 |
| depth | Float, 1 dp | 6 | 60 | 20 |
| twist | Float, 0 dp | −360 | 360 | 0 |
| taper | Float, 2 dp | 0.2 | 2.0 | 1.0 |
| lean | Float, 1 dp | 0 | 40 | 0 |
| lean_dir | Float, 0 dp | 0 | 360 | 0 |

## 2 · Tower geometry

All inputs below come from **Unpack's outputs**, never from the sliders directly. For every Expression component, zoom in to add or rename its variables.

1. **Series** (Sets › Sequence): S = 0, N = 1, C = `floors` → the floor indices **i**.
2. **Expression** "t": variables `x` = i, `y` = floors; expression `x / max(y - 1, 1)`. This runs from 0 at the ground floor to 1 at the top.
3. **Base rectangle, centred on the origin:**
   - Expression `-x/2` (x = width) and Expression `-x/2` (x = depth)
   - → **Construct Point** (X, Y, 0)
   - → **XY Plane** (Vector › Plane), origin = that point
   - → **Rectangle** (Curve › Primitive): Plane = that plane, X Size = width, Y Size = depth
4. **Expression** "scale": variables `a` = taper, `t`; expression `1 + (a - 1) * t`.
5. **Scale** (Transform › Affine): Geometry = rectangle, Centre = leave the default (origin), Factor = scale.
6. **Expression** "angle": variables `a` = twist, `t`; expression `a * t * Pi / 180` (radians).
7. **Rotate** (Transform › Euclidean): Geometry = scaled rectangles, Angle = angle (leave the *Degrees* option off), Plane = leave the default (World XY).
8. **Expressions** for the move:
   - "dx": `l * t * Sin(d * Pi / 180)`
   - "dy": `l * t * Cos(d * Pi / 180)`
   - "dz": `i * h`

   Here `l` = lean, `d` = lean_dir, `t`, `i` = Series, `h` = floor_height.
9. **Vector XYZ** (Vector › Vector): X = dx, Y = dy, Z = dz.
10. **Move** (Transform › Euclidean): Geometry = rotated rectangles, Motion = vector. This output is the list of **floor outlines**.
11. **Preview masses** (display only):
    - **Boundary Surfaces** (Surface › Freeform), with the Edges input **grafted**, from the floor outlines.
    - **Extrude** (Surface › Freeform): Base = surfaces, Direction = **Unit Z** with factor = floor_height.
    - Optionally a **Custom Preview** with a warm grey material.

Every list here has one item per floor; no data trees are needed except the graft in step 11.

## 3 · Bridge out

| Component | Settings |
|---|---|
| Panel | Text: `floor_height` |
| **Writer** (GhPython Script) | Paste [kit/gh/writer.py](../../kit/gh/writer.py). Inputs: `job` (Item, str) from Listener.job; `curves` (**List** access, type hint **Curve**) from the floor outlines (the Move output, not grafted); `keys` (List, str) from the Panel; `values` (List, float) from Unpack.floor_height. Output: `status` → Panel |

## Test it

1. Save as `examples/tower/tower.gh`, with Agent control = True.
2. Run `uv run kit ping`. The expected answer is: *Grasshopper is listening: system 'tower', Agent control ON*.
3. Run `uv run tower generate --floors 20 --twist 90 --taper 0.6 --label "gh test"`. The viewport should jump to the new tower, the Writer status should read *Sent job …*, the command should print a summary with `"backend": "grasshopper"`, and `warnings` should be empty. A warning about floor area means the definition differs from the spec.
4. Set Agent control = False and generate again. You should get a clear error saying *Agent control is OFF*.
