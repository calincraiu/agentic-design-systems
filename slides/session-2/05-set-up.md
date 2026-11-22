<!-- layout: task | where: code-yours | time: 10 min -->
<p class="kicker">Part 1 · A Grasshopper tool · your turn</p>

# Connect Claude to Rhino

1. **Open** Rhino 8 or 9.
2. **Take** the `gh` kit (below).
3. In the Code tab, **your folder**, new session: ask *"What's open in Rhino right now?"*

<div data-widget="takeaway" data-kit="gh"></div>

> **You're done when** Claude's answer came from Rhino: you can open a Rhino tool call in its reply.

<!-- notes -->
#### What you're building
A link between Claude and Rhino, and the runner that will run every Grasshopper tool you make. There are no tools in your folder yet.

#### Steps
1. **Open** Rhino 8 or 9, and leave it open.
2. **Take** the `gh` kit with the prompt on the slide, in the Code tab, in your own folder.
3. **Start** a new session and ask *"What's open in Rhino right now?"*
4. **Expand** the tool call in Claude's reply. *If there's no Rhino tool call, Claude guessed.*
    - If Claude says it has no Rhino tools: the MCP server isn't connected to the desktop app. Go back to the setup checklist.
    - If Claude opens a second Rhino: close both and let Claude start one. The tools work the same either way.

#### Background
Claude talks to Rhino through RhinoAI's **MCP server**. MCP (Model Context Protocol) is a standard way for an app like Claude to offer the model extra tools. The Rhino server's tools can read what's in Rhino, take a picture of a viewport, and run a Python script inside Rhino. Each use shows in the reply as a tool call, like a `uv run` command in Session 1.

The `gh` kit contains:

- `tools/grasshopper/runner.py`: the **runner**, which runs any Grasshopper tool. You don't need to read it.
- `tools/grasshopper/TEMPLATE.md`: a blank contract for a Grasshopper tool.
- `.claude/skills/grasshopper/SKILL.md`: how Claude runs these tools.

The kit's `.claude/settings.json` lets Claude read Rhino's state and take viewport pictures without asking. Running a script in Rhino still asks every time. If your folder already has a `settings.json` from Session 1, keep yours: the only difference is a few more permission prompts.
