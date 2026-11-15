<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The tool</p>

# A command is a button with typed inputs

<div data-widget="figure" data-name="command"></div>

> You won't type these. Claude will, and it shows you each one before it runs it.

<!-- notes -->
**The idea.** A **command** is one line that runs a tool. Read it left to right:

1. `uv run`: start a tool. `uv` is a small program that runs Python tools and fetches anything they need.
2. `tools/add.py`: which tool. It's a file in your folder, found by its path: the `tools` folder, then the file `add.py`.
3. `48213.5 99127.25`: the inputs. Some tools name their inputs instead, like `--sides 6 --count 2` for the dice. That's the same idea, with labels.
4. What comes back: the tool prints its answer, and Claude reads it.

**Why it matters.** In the Code tab, Claude shows you a command like this before it runs it, and asks for permission if it hasn't been allowed before. The kits allow `uv run tools/...` from the start, so their tools run without asking. Anything else, Claude asks first. Reading a command tells you which tool and which inputs. That's enough to judge whether to allow it.

**Try it yourself.** Open "Behind the scenes" under any widget in this app. It shows the exact command the agent would type, and the tool's raw answer.
