---
name: setup-course
description: Sets up and checks a student's computer for the course. Installs uv, prepares the course app, tests the add, dice and tower tools, and (from Session 2) checks that Claude can reach Rhino, Grasshopper and Ladybug. Use when the student says setup, install, get started, or that something isn't working.
---

# Setup

Get this computer ready for the course, explaining each step in one plain sentence as you go. This is often the student's first time watching an agent act on their machine, so say what each command does **before** running it.

## Steps

1. **uv** (the program that installs and runs Python for the course). Run `uv --version`.
   - If it's missing, explain what it is and ask permission to install it:
     - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
     - Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - If `uv` still isn't found afterwards, ask the student to restart the app and run `/setup-course` again.
2. **Course app.** Run `uv sync`. The first time, it downloads Python and the libraries, which takes a minute.
3. **Add and dice tools.** Run `uv run kits/add/tools/add.py 2 2` and `uv run kits/dice/tools/dice.py --count 2`, and show the results.
4. **Tower tool.** Run `uv run kits/tower/tools/tower/tower.py --floors 8 --label "setup test"`. It should print metrics and an image path.
5. **Rhino (Session 2 on).** Ask whether the student has Rhino 8 or 9 installed. If not, skip to the summary: Session 1 doesn't need it.
   - **Rhino tools.** Use the Rhino MCP tool `get_context`. If you have no Rhino tools at all, the RhinoAI MCP server isn't connected to this app: say so, and point the student to the Session 2 setup checklist. Don't try to install or configure it yourself.
   - **Grasshopper.** With the Rhino MCP tool `run_python`, send exactly this script, with this folder's full path (forward slashes). It should print `sum = 3`:
     ```python
     import runpy
     runner = runpy.run_path(r"<this folder>/kits/gh/tools/grasshopper/runner.py")
     runner["run"](r"<this folder>/kits/sum/tools/sum/sum.gh", {"a": 1, "b": 2}, __rhino_doc__, receipt=False)
     ```
   - **Ladybug.** Send the same script with the last line changed to `runner["run"](r"<this folder>/kits/measures/tools/park_sun/park_sun.gh", {"city": "London"}, __rhino_doc__, bake=False, receipt=False)`. A `location` line starting `London, lat:51.51` means Ladybug works (warnings about missing geometry are expected). An error saying "No module named ladybug" on **Rhino 9** is the known Ladybug installer gap: point the student to the Ladybug section of the setup checklist.
6. **Summary.** Give a short checklist of what works and anything still to fix. If everything works, tell the student to type `/start-course` to open the course app.

## Rules

- Don't create or edit files in this folder. Running the steps above is all setup needs. The Rhino checks pass `receipt=False`, so they leave nothing behind.
