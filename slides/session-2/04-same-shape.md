<!-- layout: stage | where: app -->
<p class="kicker">Part 1 · A Grasshopper tool</p>

# Same tool, new engine

| | Session 1 · `add.py` | Today · `sum.gh` |
|---|---|---|
| **The tool** | a Python file | a Grasshopper definition |
| **Inputs** | numbers after the command | sliders nicknamed `in:a`, `in:b` |
| **What it accepts** | the script refuses `1,5` | the runner refuses what the slider can't take |
| **How Claude runs it** | `uv run tools/add.py …` | three lines sent to Rhino |
| **The record** | the command and its output | a receipt in `runs/` |
| **The contract** | `--help` | `sum.md`, next to `sum.gh` |

<!-- notes -->
Every row on the left has a partner on the right. That's why you don't need a new idea of a tool for Grasshopper, only a new way to name its parts.

The biggest difference is where the limits live. In `add.py` the refusal is written in the code. In a Grasshopper tool it's set on the canvas: a Number Slider's minimum, maximum and decimal places are exactly what the tool accepts, and a Value List's item names are its allowed choices. You change what a tool accepts by changing the slider, in Grasshopper.

The other difference is who runs it. `add.py` runs in your folder. A `.gh` file can only run inside Rhino, so Claude sends Rhino a short script that opens the definition, sets the inputs and reads the outputs.
