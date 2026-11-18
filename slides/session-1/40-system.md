<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · All together</p>

# Six parts, one system

<div data-widget="figure" data-name="parts" data-start="5"></div>

> A skill shapes how the agent works. Context is what it has in front of it. **You** decide what is good.

<!-- notes -->
Part 1 in six lines:

1. An **LLM** writes text that is likely to fit. It recalls 2 + 2, but it can't be relied on to calculate exactly or to choose fairly.
2. A **tool** does one exact thing. `add.py` adds and `dice.py` rolls.
3. An **agent** is an LLM that uses tools and decides what to do next, as when it rolled until a double.
4. A **skill** is know-how in plain text. `add-up` never adds in its head, and `tie-breaker` rolls exactly once.
5. **Context** is what the agent has in front of it. Your `CLAUDE.md` is the part that's there before you ask anything.
6. **You** decide what counts as good.

That makes five parts, plus you. All of it runs inside the **app**, which loads the context, runs the tools and asks you before acting. The model, in a data centre, only writes text.

Larger systems are built from the same parts. When something goes wrong, the first question is which part was responsible: the tool, the skill's instructions, the context, or the model improvising.

To revise, name today's example for each part without looking, then check against the concepts page (Reference, on the app's index page).
