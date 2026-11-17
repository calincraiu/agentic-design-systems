<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · All together</p>

# Six parts, one system

<div data-widget="figure" data-name="parts" data-start="5"></div>

> A skill shapes how the agent works. Context is what it has in front of it. **You** decide what is good.

<!-- notes -->
**The idea.** Here is Part 1 in six sentences:

1. An **LLM** writes text that fits. It recalls 2 + 2, but it can't be relied on to calculate exactly, or to be fair.
2. A **tool** does one exact thing: `add.py` adds, `dice.py` rolls.
3. An **agent** is an LLM that can use tools and decide what to do next, like rolling until a double.
4. A **skill** is know-how in plain text: `add-up` never adds in its head, and `tie-breaker` rolls exactly once.
5. **Context** is what the agent has in front of it while it works. Your `CLAUDE.md` is the part that's there before you ask.
6. **You** decide what is good. That is design.

All of it runs inside the **app**: it loads the context, runs the tools and asks you before acting. The model, far away, only writes.

**Why it matters.** Every agentic design system you build, however big, is made of these same six parts. When something goes wrong, the first question is *which part* was responsible. Was it the tool, the skill's instructions, the context, or the LLM improvising?

The next slide practises exactly that.

**Try it yourself.** For each part, name the example from today without looking. Then open `slides/concepts.md` in the course app (Reference, on the index page) to check.
