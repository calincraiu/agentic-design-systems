"""The Grasshopper runner: runs a .gh file as a tool, inputs in, outputs out.

It runs *inside Rhino*. Claude sends Rhino a three-line script through the Rhino
MCP server (see the grasshopper skill):

    import runpy
    runner = runpy.run_path(r"<your folder>/tools/grasshopper/runner.py")
    runner["run"](r"<your folder>/tools/sum/sum.gh", {"a": 12.5, "b": 30}, __rhino_doc__)

How a definition becomes a tool: on the canvas, anything whose nickname starts
with "in:" is an input, and anything starting with "out:" is an output.

  in:   a Number Slider (its min and max are the allowed range), a Value List (its
        item names are the allowed choices), a Boolean Toggle, a Panel (text), or any
        parameter (a number, some text, or "layer:Site::Park" for the objects on that
        Rhino layer)
  out:  any parameter or Panel. Numbers and text are reported; geometry is baked
        to the layer runs::<tool>::<run>

The runner opens the file without showing it, never changes it, and writes a
receipt to runs/ in your folder.
"""
import json
import math
import re
from datetime import datetime
from pathlib import Path

IN, OUT = "in:", "out:"


# Plain Python: checks and receipts (tested without Rhino) ----------------------


def check_slider_value(name, value, low, high, decimals, kind="float"):
    """Return a problem (text) if a slider can't take this value exactly, or None.

    A Grasshopper slider silently clamps and rounds whatever it is given. A tool
    must refuse instead.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return f"{name} must be a number (got {value!r})"
    if not low <= value <= high:
        return f"{name} = {value:g} is outside {low:g} to {high:g} (the slider's range)"
    steps = value * 10 ** decimals
    if abs(steps - round(steps)) > 1e-6:
        if decimals == 0:
            return f"{name} must be a whole number (got {value:g})"
        return f"{name} = {value:g} has more than {decimals} decimal places (the slider's precision)"
    if kind == "even" and round(value) % 2:
        return f"{name} must be an even number (got {value:g})"
    if kind == "odd" and not round(value) % 2:
        return f"{name} must be an odd number (got {value:g})"
    return None


def choose(name, value, options):
    """Find value among a Value List's item names, ignoring case. Returns (index, problem)."""
    wanted = str(value).strip().lower()
    for i, option in enumerate(options):
        if option.strip().lower() == wanted:
            return i, None
    return None, f"{name} = {value!r} is not one of its choices: {', '.join(options)}"


def layer_ref(value):
    """'layer:Site::Park' -> 'Site::Park'. Anything else -> None."""
    if isinstance(value, str) and value.startswith("layer:"):
        return value[len("layer:"):].strip()
    return None


def project_folder(gh_path):
    """The folder that contains tools/ (the student's folder), found from the .gh path."""
    path = Path(gh_path).resolve()
    for parent in path.parents:
        if parent.name == "tools":
            return parent.parent
    return path.parent


def safe_name(text):
    return re.sub(r"[^A-Za-z0-9_-]+", "-", str(text)).strip("-")[:40] or "run"


def receipt_path(folder, tool, label=None, now=None):
    """runs/<date>_<time>_<tool>[_<label>].json, numbered if that name is taken."""
    stamp = (now or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
    name = f"{stamp}_{safe_name(tool)}" + (f"_{safe_name(label)}" if label else "")
    path, n = Path(folder) / "runs" / f"{name}.json", 2
    while path.exists():
        path, n = Path(folder) / "runs" / f"{name}_{n}.json", n + 1
    return path


def plain(value):
    """A value as it should appear in the receipt: numbers as numbers where possible."""
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
        if not math.isfinite(number):
            return value
        return int(number) if number.is_integer() and "." not in value else number
    return value


def number(value):
    """12.0 -> '12', 8479.117241 -> '8479.12'; anything else unchanged."""
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".") if abs(value) >= 1 else f"{value:.4g}"
    if isinstance(value, list):
        return "[" + ", ".join(number(v) for v in value) + "]"
    return value


def summary(receipt):
    """The few lines printed after a run, for Claude and the student to read."""
    lines = [f"Grasshopper tool: {receipt['tool']} ({receipt['file']})"]
    if receipt.get("refused"):
        lines += ["REFUSED, nothing was run:"] + [f"  - {p}" for p in receipt["refused"]]
        if receipt.get("inputs_available"):
            lines.append("Inputs it takes: " + ", ".join(receipt["inputs_available"]))
        return "\n".join(lines)
    shown = [f"{k} = {number(v['value'])}" + ("" if v["given"] else " (default)") for k, v in receipt["inputs"].items()]
    lines.append("Inputs:  " + (", ".join(shown) or "none"))
    for k, v in receipt["outputs"].items():
        if isinstance(v, dict) and "baked" in v:
            lines.append(f"Output:  {k} = {v['count']} object(s), baked to layer {v['baked']}")
        else:
            lines.append(f"Output:  {k} = {number(v)}")
    if receipt.get("hidden"):
        lines.append(f"Shown:   only this run; {receipt['hidden']} earlier run(s) of {receipt['tool']} hidden, not deleted")
    for w in receipt.get("warnings", []):
        lines.append(f"WARNING: {w}")
    for e in receipt.get("errors", []):
        lines.append(f"ERROR:   {e}")
    if receipt.get("geometry"):
        lines.append(f"Units:   {receipt['units']}")
    lines.append(f"Receipt: {receipt['receipt']}")
    return "\n".join(lines)


# Inside Rhino ------------------------------------------------------------------


def _grasshopper():
    import Rhino
    Rhino.RhinoApp.GetPlugInObject("Grasshopper")  # loads Grasshopper without opening its window
    import Grasshopper
    return Grasshopper


def _open(gh_path):
    gh = _grasshopper()
    io = gh.Kernel.GH_DocumentIO()
    if not io.Open(str(gh_path)):
        raise FileNotFoundError(f"Grasshopper could not open {gh_path}")
    return io.Document


def _named(document, prefix):
    found = {}
    for obj in document.Objects:
        nick = (obj.NickName or "").strip()
        if nick.lower().startswith(prefix):
            found[nick[len(prefix):].strip()] = obj
    return found


def _kind(obj):
    name = type(obj).__name__
    gh = _grasshopper()
    special = gh.Kernel.Special
    if isinstance(obj, special.GH_NumberSlider):
        return "slider"
    if isinstance(obj, special.GH_BooleanToggle):
        return "toggle"
    if isinstance(obj, special.GH_Panel):
        return "panel"
    if isinstance(obj, special.GH_ValueList):
        return "choice"
    return "param" if hasattr(obj, "PersistentData") else name


def _slider_info(slider):
    import System
    s = slider.Slider
    kind = str(s.Type).lower()  # Float, Integer, Even, Odd
    return {"low": System.Decimal.ToDouble(s.Minimum), "high": System.Decimal.ToDouble(s.Maximum),
            "decimals": 0 if kind != "float" else int(s.DecimalPlaces), "kind": kind,
            "value": System.Decimal.ToDouble(s.Value)}


def _describe_input(obj):
    kind = _kind(obj)
    if kind == "slider":
        i = _slider_info(obj)
        places = {0: ", whole numbers", 1: ", 1 decimal place"}.get(i["decimals"], f", {i['decimals']} decimal places")
        return f"number from {i['low']:g} to {i['high']:g}{places} (now {i['value']:g})"
    if kind == "toggle":
        return f"true or false (now {obj.Value})"
    if kind == "panel":
        return "text"
    if kind == "choice":
        return f"one of: {', '.join(i.Name for i in obj.ListItems)} (now {_current_value(obj)})"
    kind = obj.GetType().Name.replace("Param_", "").lower()
    return f"{kind}: a value, or layer:<Layer::Name> for the objects on a Rhino layer"


def _goo_from_layer(rhino_doc, layer):
    gh = _grasshopper()
    index = rhino_doc.Layers.FindByFullPath(layer, -1)
    if index < 0:
        raise ValueError(f"there is no layer called {layer} in this Rhino file")
    objects = rhino_doc.Objects.FindByLayer(rhino_doc.Layers[index]) or []
    if not objects:
        raise ValueError(f"layer {layer} is empty")
    return [gh.Kernel.GH_Convert.ToGoo(o.Geometry.Duplicate()) for o in objects]


def _set_input(name, obj, value, rhino_doc):
    """Set one input. Returns a problem (text) or None."""
    import System
    gh = _grasshopper()
    kind = _kind(obj)
    if kind == "slider":
        i = _slider_info(obj)
        problem = check_slider_value(name, value, i["low"], i["high"], i["decimals"], i["kind"])
        if problem:
            return problem
        obj.SetSliderValue(System.Decimal(value))
        return None
    if kind == "toggle":
        if not isinstance(value, bool):
            return f"{name} must be true or false (got {value!r})"
        obj.Value = value
        return None
    if kind == "panel":
        obj.UserText = str(value)
        return None
    if kind == "choice":
        index, problem = choose(name, value, [i.Name for i in obj.ListItems])
        if problem:
            return problem
        obj.SelectItem(index)
        return None
    values = value if isinstance(value, list) else [value]
    goo = []
    for v in values:
        layer = layer_ref(v)
        if layer is not None:
            try:
                goo += _goo_from_layer(rhino_doc, layer)
            except ValueError as e:
                return f"{name}: {e}"
        else:
            goo.append(gh.Kernel.GH_Convert.ToGoo(v))
    obj.PersistentData.Clear()
    for g in goo:
        obj.PersistentData.Append(g)
    return None


def _current_value(obj):
    kind = _kind(obj)
    if kind == "slider":
        return _slider_info(obj)["value"]
    if kind == "toggle":
        return bool(obj.Value)
    if kind == "panel":
        return obj.UserText
    if kind == "choice":
        selected = obj.FirstSelectedItem
        return selected.Name if selected else None
    items =list(obj.PersistentData.AllData(True)) if hasattr(obj, "PersistentData") else []
    return [str(i) for i in items] if len(items) != 1 else str(items[0])


def _bake_layer(rhino_doc, path):
    import Rhino
    parent = None
    for part in path.split("::"):
        full = part if parent is None else f"{rhino_doc.Layers[parent].FullPath}::{part}"
        index = rhino_doc.Layers.FindByFullPath(full, -1)
        if index < 0:
            layer = Rhino.DocObjects.Layer()
            layer.Name = part
            if parent is not None:
                layer.ParentLayerId = rhino_doc.Layers[parent].Id
            index = rhino_doc.Layers.Add(layer)
        parent = index
    for old in rhino_doc.Objects.FindByLayer(rhino_doc.Layers[parent]) or []:  # a rerun replaces, never piles up
        rhino_doc.Objects.Delete(old, True)
    return parent


def _show_only(rhino_doc, tool_layer, run_layer):
    """Hide the earlier runs of this tool (their layers stay), show this one. Returns how many were hidden."""
    hidden = 0
    for layer in rhino_doc.Layers:
        path = layer.FullPath
        if layer.IsDeleted or path.count("::") != run_layer.count("::") or not path.startswith(tool_layer + "::"):
            continue
        visible = path == run_layer
        if layer.IsVisible != visible:
            hidden += not visible
            layer.IsVisible = visible
            layer.CommitChanges()
    return hidden


def _bake(rhino_doc, item, layer_index):
    import Rhino
    g = Rhino.Geometry
    attributes = Rhino.DocObjects.ObjectAttributes()
    attributes.LayerIndex = layer_index
    if isinstance(item, g.Point3d):
        return rhino_doc.Objects.AddPoint(item, attributes)
    for convert in ("ToBrep", "ToNurbsCurve"):  # Box, Rectangle3d, Circle, Line...
        if not isinstance(item, g.GeometryBase) and hasattr(item, convert):
            item = getattr(item, convert)()
            break
    if isinstance(item, g.GeometryBase):
        return rhino_doc.Objects.Add(item, attributes)
    return None


def _read_output(obj):
    """Returns (values, geometry): plain values, and geometry objects to bake."""
    import Rhino
    values, geometry = [], []
    for goo in obj.VolatileData.AllData(True):
        if goo is None:
            continue
        item = goo.ScriptVariable()
        if isinstance(item, (bool, int, float, str)):
            values.append(plain(item))
        elif isinstance(item, (Rhino.Geometry.GeometryBase, Rhino.Geometry.Point3d)) or hasattr(item, "ToBrep") \
                or hasattr(item, "ToNurbsCurve"):
            geometry.append(item)
        else:
            values.append(plain(str(item)))
    return values, geometry


def plain_message(nickname, message):
    """Grasshopper's warning for an input that got nothing, in plain words."""
    if nickname.lower().startswith(IN) and "failed to collect data" in message:
        return f"{nickname} was given nothing, so any output that depends on it means nothing"
    return f"{nickname}: {message}"


def _messages(document, level):
    gh = _grasshopper()
    lvl = getattr(gh.Kernel.GH_RuntimeMessageLevel, level)
    found = []
    for obj in document.Objects:
        if hasattr(obj, "RuntimeMessages"):
            for m in obj.RuntimeMessages(lvl):
                found.append(plain_message(obj.NickName, m))
    return found


def describe(gh_path):
    """Print what a Grasshopper tool takes and gives, without running it."""
    document = _open(gh_path)
    try:
        lines = [f"Grasshopper tool: {Path(gh_path).stem}"]
        inputs, outputs = _named(document, IN), _named(document, OUT)
        lines += ["Inputs:"] + [f"  {k}: {_describe_input(o)}" for k, o in inputs.items()] if inputs else ["Inputs: none"]
        lines += ["Outputs:"] + [f"  {k}" for k in outputs] if outputs else ["Outputs: none (add out: to a nickname)"]
        print("\n".join(lines))
    finally:
        document.Dispose()


def run(gh_path, inputs, rhino_doc, label=None, bake=True, receipt=True):
    """Run a Grasshopper tool once. Prints a summary and writes a receipt to runs/ (receipt=False: a check that
    keeps no record, for /setup-course)."""
    keep = receipt
    gh = _grasshopper()
    gh_path = Path(gh_path).resolve()
    folder = project_folder(gh_path)
    tool = gh_path.stem
    path = receipt_path(folder, tool, label)
    receipt = {"tool": tool, "file": gh_path.relative_to(folder).as_posix() if folder in gh_path.parents
               else str(gh_path), "label": label, "time": datetime.now().isoformat(timespec="seconds"),
               "units": str(rhino_doc.ModelUnitSystem), "receipt": path.relative_to(folder).as_posix()}
    document = _open(gh_path)
    try:
        slots_in, slots_out = _named(document, IN), _named(document, OUT)
        problems = [f"'{k}' is not an input of this tool" for k in inputs if k not in slots_in]
        if not slots_out:
            problems.append("the definition has no outputs (nothing has a nickname starting with out:)")
        for name, value in inputs.items():
            if name in slots_in:
                problem = _set_input(name, slots_in[name], value, rhino_doc)
                if problem:
                    problems.append(problem)
        if problems:
            receipt["refused"] = problems
            receipt["inputs_available"] = sorted(slots_in)
            print(summary(receipt))
            return
        receipt["inputs"] = {k: {"value": inputs[k] if k in inputs else _current_value(o), "given": k in inputs}
                             for k, o in slots_in.items()}

        document.Enabled = True
        document.NewSolution(True, gh.Kernel.GH_SolutionMode.Silent)

        receipt["outputs"], receipt["warnings"] = {}, _messages(document, "Warning")
        receipt["errors"] = _messages(document, "Error")
        uses_geometry = any(layer_ref(v) for v in inputs.values() if not isinstance(v, list)) or any(
            layer_ref(x) for v in inputs.values() if isinstance(v, list) for x in v)
        run_layer = f"runs::{safe_name(tool)}::{safe_name(label or receipt['time'].replace(':', ''))}"
        for name, obj in slots_out.items():
            values, geometry = _read_output(obj)
            if geometry:
                uses_geometry = True
                if bake:
                    layer = f"{run_layer}::{safe_name(name)}"
                    index = _bake_layer(rhino_doc, layer)
                    baked = [_bake(rhino_doc, g, index) for g in geometry]
                    receipt["outputs"][name] = {"count": sum(1 for b in baked if b), "baked": layer}
                else:
                    receipt["outputs"][name] = {"count": len(geometry), "baked": None}
            else:
                receipt["outputs"][name] = values[0] if len(values) == 1 else values
        receipt["geometry"] = uses_geometry
        if uses_geometry and "meter" not in receipt["units"].lower():
            receipt["warnings"].append(f"this Rhino file is in {receipt['units']}, and the course tools expect metres")
        if bake and uses_geometry:
            receipt["hidden"] = _show_only(rhino_doc, f"runs::{safe_name(tool)}", run_layer)
            rhino_doc.Views.Redraw()
    finally:
        document.Enabled = False
        document.Dispose()

    if keep:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(receipt, indent=2, default=str), encoding="utf-8")
    else:
        receipt["receipt"] = "none (a check, not kept)"
    print(summary(receipt))
