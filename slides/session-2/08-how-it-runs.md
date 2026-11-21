<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · Tool</p>

# The model writes three lines, Rhino runs them

<div data-widget="figure" data-name="runner" data-start="0" data-ghost></div>

<!-- notes -->
This is the same split you saw in Session 1, where the model asks and the app acts, with Rhino in the place of your folder. The model writes a short script and asks the app to run it in Rhino. For every tool it's the same three lines; only the file name and the values change:

```python
import runpy
runner = runpy.run_path(r"<your folder>/tools/grasshopper/runner.py")
runner["run"](r"<your folder>/tools/tower/tower.gh", {"floors": 30}, __rhino_doc__, label="A")
```

The **runner** opens the `.gh` file without showing it on screen. It finds every input whose nickname starts with `in:` and every output starting with `out:`. It sets the inputs, lets Grasshopper solve, and reads the outputs. Geometry is baked into Rhino on a layer of its own, such as `runs::tower::A`. The runner also writes a **receipt**, a file in `runs/` with every input and output, and prints the results so they go back to the model as text.

The runner refuses a value a slider can't take. A Grasshopper slider quietly clamps a value outside its range: give a 0–1000 slider 2000 and it uses 1000 without a word. It also rounds a value with too many decimals. A tool has to refuse instead, as `add.py` refused `1,5` in Session 1.
