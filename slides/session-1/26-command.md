<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The tool</p>

# A command is a button with typed inputs

<div data-widget="figure" data-name="command"></div>

> You won't type these. Claude will, and it shows you each one before it runs it.

<!-- notes -->
A **command** is one line that runs a tool. From left to right:

1. `uv run` starts a Python tool. `uv` is a small program that runs Python tools and downloads anything they need.
2. `tools/add.py` says which tool, by its path in your folder.
3. `48213.5 99127.25` are the inputs. Some tools label their inputs instead, like `--sides 6 --count 2` for the dice tool.
4. The tool prints its answer, and Claude reads it.

In the Code tab, Claude shows each command before it runs. If that kind of command hasn't been allowed yet, the app asks you first. The kits allow `uv run tools/...` from the start, so the course tools run without asking, and anything else gets a prompt. The command tells you which tool and which inputs, which is usually enough to decide whether to allow it.

Open "Behind the scenes" under any widget in this app to see the exact command and the tool's raw output.
