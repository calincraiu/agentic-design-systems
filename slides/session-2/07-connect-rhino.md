<!-- layout: task | where: code-yours | time: 10 min -->
<p class="kicker">Part 1 · Tool · your turn</p>

# Connect Claude to Rhino

1. **Open** Rhino 8 or 9.
2. In the Code tab, **your folder**, new session: ask *"What's open in Rhino right now?"*
3. **Take** the `gh` kit (below).
4. **Check** that `tools/grasshopper`, `tools/sum` and `.claude/skills/grasshopper` arrived.

<div data-widget="takeaway" data-kit="gh"></div>

> **You're done when** Claude's answer came from Rhino: you can open a Rhino tool call in its reply.

<!-- notes -->
Claude talks to Rhino through RhinoAI's **MCP server**. MCP (Model Context Protocol) is a standard way for an app like Claude to offer the model extra tools. The Rhino server's tools can read what's in Rhino, take a picture of a viewport, and run a Python script inside Rhino. When Claude uses one, the reply shows a tool call you can expand, just like a `uv run` command in Session 1. If the answer has no Rhino tool call in it, Claude guessed.

If Claude says it has no Rhino tools, the MCP server isn't connected to the desktop app: go back to the setup checklist. If it opens a second Rhino instead of using yours, close both and let Claude start one; the tools work the same either way.

The `gh` kit contains:

- `tools/grasshopper/runner.py`: the **runner**, which runs any Grasshopper tool. You don't need to read it.
- `tools/grasshopper/TEMPLATE.md`: a blank contract for a Grasshopper tool.
- `tools/sum/sum.gh` and `sum.md`: the smallest possible tool, which adds two numbers, and its contract.
- `.claude/skills/grasshopper/SKILL.md`: how Claude runs these tools.

The kit's `.claude/settings.json` lets Claude read Rhino's state and take viewport pictures without asking. Running a script in Rhino still asks every time. If your folder already has a `settings.json` from Session 1, keep yours: the only difference is a few more permission prompts.
