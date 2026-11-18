<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The agent</p>

# One answer stops. An agent keeps going.

<div data-widget="figure" data-name="agent-loop" data-start="1"></div>

<!-- notes -->
A single question gets a single answer, and then the model waits for you. An agent is given a goal and goes round a loop by itself:

1. **Act.** It uses a tool, for example running a command, reading a file or making something.
2. **Look.** It reads what came back.
3. **Decide.** If the goal isn't met, it acts again using what it just learned. If it is, it stops and reports.

The LLM does the looking and deciding, and a tool does the acting. You are involved at the two ends, setting the goal and reading the report.

There is no list of steps in the diagram, because nobody writes one in advance. The number of rounds depends on what each result turns out to be. A lot of design work has this try, look, adjust shape, and an agent can run it quickly, but the decision to stop is still the model's judgement.

You may have seen Chat run a calculation on the way to an answer. That is a small loop too, in Chat's own workspace with its own tools. In the Code tab the loop runs in your folder, with your tools, your skills and your `CLAUDE.md`, which are the parts you can write and change.

Think of a task you do by trying, looking and adjusting, such as setting out a stair, adjusting a facade grid or checking a drawing set. Which steps would you hand to an agent, and which would you keep?
