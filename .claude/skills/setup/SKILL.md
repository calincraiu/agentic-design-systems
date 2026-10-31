---
name: setup
description: Sets up and checks a student's computer for the course. Installs the Python environment with uv, then tests the dice and tower tools. Use when the student says setup, install, get started, or that something isn't working.
---

# Setup

Get this computer ready for the course, explaining each step in one plain sentence as you go. This is often the student's first time watching an agent act on their machine, so be clear about what each command does **before** running it.

## Steps

1. **uv** (the tool that manages Python for this project). Run `uv --version`.
   - If it's missing, explain what it is and ask permission to install it:
     - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
     - Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - If `uv` still isn't found afterwards, ask the student to restart the app and run `/setup` again.
2. **Project environment.** Run `uv sync`. It downloads Python and the libraries the first time, which takes a minute.
3. **First tool.** Run `uv run tools/dice.py --count 2`, and show the student the result.
4. **First tower.** Run `uv run tools/tower.py --project "Setup test" --skill setup --label "setup test" --why "checking the setup"`. Look at the image it reports, using the Read tool.
5. **Gallery.** Tell the student to click `runs/gallery.html` in your message to open it. If that doesn't open it, run `uv run tools/gallery.py --open`.
6. **Summary.** Give a short checklist of what works and anything still to fix.
