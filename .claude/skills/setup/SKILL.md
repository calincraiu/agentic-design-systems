---
name: setup
description: Sets up and checks a student's computer for the course. Installs the Python environment with uv, runs the checks, makes a first test tower and tests the Grasshopper connection. Use when the student says setup, install, get started, or that something isn't working.
---

# Setup

Get this computer ready for the course, explaining each step in one plain sentence as you go. This is often the student's first time watching an agent act on their machine, so be clear about what each command does **before** running it.

## Steps

1. **uv** (the tool that manages Python for this project). Run `uv --version`.
   - If it's missing, explain what it is and ask permission to install it:
     - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
     - Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Afterwards VS Code may need restarting so it can find `uv`.
2. **Project environment.** Run `uv sync`. It downloads Python and the libraries the first time, which takes a minute.
3. **Checks.** Run `uv run kit doctor` and fix any `[!!]` lines. `[--] Grasshopper is not listening` is fine at this stage.
4. **First tower, without Rhino.** Run `uv run tower generate --backend python --skill setup --label "setup test" --why "checking the setup"`. Show the student the image (Read it) and open the gallery with `uv run kit gallery --open`.
5. **Grasshopper.** Ask the student to:
   1. open Rhino 8, then Grasshopper
   2. open `examples/tower/tower.gh` from the repo folder (not a copy elsewhere)
   3. check that the **Agent control** toggle is True

   Then run `uv run kit ping`. If there's no answer, use the troubleshooting table in `kit/gh/README.md`.
6. **First tower through Grasshopper.** Tell the student to watch the Rhino viewport, then run `uv run tower generate --skill setup --label "hello grasshopper" --floors 20 --twist 90 --taper 0.6`.
7. **Summary.** Give a short checklist of what works and anything still to fix.
