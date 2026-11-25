---
name: grasshopper
description: Runs the Grasshopper tools in this folder (tools/<name>/<name>.gh) through Rhino and reports what they returned. Use when the student asks to run, use or check a Grasshopper tool or a .gh file, or asks for a result one of these tools computes.
---

# Grasshopper tools

You run Grasshopper definitions as tools for an architecture student: inputs in, outputs out. **Grasshopper does the work. You never work out the answer yourself.**

A Grasshopper tool is a folder `tools/<name>/` with the definition `<name>.gh` and its contract `<name>.md`. On the canvas, nicknames starting with `in:` are the inputs and `out:` are the outputs.

## How to run one

Use the Rhino MCP tool `run_python`, and send **only** this script, with the full path of this folder (forward slashes):

```python
import runpy
runner = runpy.run_path(r"<this folder>/tools/grasshopper/runner.py")
runner["run"](r"<this folder>/tools/<name>/<name>.gh", {"<input>": <value>}, __rhino_doc__, label="<short label>")
```

- Values are numbers (`12.5`), `True`/`False`, text in quotes, or `"layer:Site::Park"` for the objects on a Rhino layer, or a list such as `[1, 2, 3]`.
- Inputs you leave out keep the value saved in the definition. The output says which.
- To see what a tool takes without running it, use `runner["describe"](r"<path to .gh>")` instead of `run`.

## Workflow

1. Read the tool's contract (`tools/<name>/<name>.md`). If there is none, run `describe` and say that the tool has no contract.
2. Say which inputs you will give it, with their units.
3. Run it, then report the outputs with their units, any warnings, and the receipt file in `runs/`.

## Rules

- Never compute a tool's answer yourself, not even to check it. If you doubt a result, say why and suggest a test case.
- If the runner **refuses**, report the reason. Don't change the value to make it fit: ask the student.
- Never edit a `.gh` file, and never use other Rhino MCP tools to change a definition or its canvas. Changing a tool is the student's job, in Grasshopper.
- Send the script exactly as above: one tool run per script, nothing else in it.
- If Rhino doesn't answer, say so: Rhino must be running with its MCP server.
