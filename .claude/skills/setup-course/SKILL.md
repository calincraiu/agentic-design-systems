---
name: setup-course
description: Sets up and checks a student's computer for the course. Installs uv, prepares the course app, and tests the add, dice and tower tools. Use when the student says setup, install, get started, or that something isn't working.
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
5. **Summary.** Give a short checklist of what works and anything still to fix. If everything works, tell the student to type `/start-course` to open the course app.

## Rules

- Don't create or edit files in this folder. Running the steps above is all setup needs.
