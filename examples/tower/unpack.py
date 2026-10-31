"""
Tower Toy - Unpack  (paste into a GhPython / Python Script component)

Decides where the tower's parameters come from: the agent's job, when there is
one, or otherwise the sliders.

Inputs (all Item access)
  job                  str    from the Listener
  slider_floors        int    from the "floors" slider
  slider_floor_height  float  ... and one input per slider, named slider_<parameter>
  slider_width, slider_depth, slider_twist, slider_taper, slider_lean, slider_lean_dir
Outputs
  floors, floor_height, width, depth, twist, taper, lean, lean_dir   the values to build with
  source   "agent" or "sliders"

Runs in Rhino 7 (IronPython 2.7) and Rhino 8 (Python 3).
"""
import json

values = {
    "floors": slider_floors,  # noqa: F821 (inputs come from Grasshopper)
    "floor_height": slider_floor_height,  # noqa: F821
    "width": slider_width,  # noqa: F821
    "depth": slider_depth,  # noqa: F821
    "twist": slider_twist,  # noqa: F821
    "taper": slider_taper,  # noqa: F821
    "lean": slider_lean,  # noqa: F821
    "lean_dir": slider_lean_dir,  # noqa: F821
}
source = "sliders"
if job:  # noqa: F821
    params = json.loads(job).get("params", {})  # noqa: F821
    for name in values:
        if name in params:
            values[name] = params[name]
    source = "agent"

floors = int(values["floors"])
floor_height = float(values["floor_height"])
width = float(values["width"])
depth = float(values["depth"])
twist = float(values["twist"])
taper = float(values["taper"])
lean = float(values["lean"])
lean_dir = float(values["lean_dir"])
