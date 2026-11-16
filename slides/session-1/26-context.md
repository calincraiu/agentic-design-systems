<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · Context</p>

# Context is what the agent knows before you ask

<div data-widget="context"></div>

> Demo: add *"Announce every dice result like an excited sports commentator"* to `CLAUDE.md`, start a **new session** and roll.

<!-- notes -->
**The idea.** **Context** is everything the agent knows while it works: your project instructions, the files it has read, and the conversation so far. Step through the widget and watch what is there at each moment.

The important step is the last one. When you start a **new session**, the conversation, the skill's full text and the tool's answers are gone. Of everything *you* wrote, only two things come back every time:

- your `CLAUDE.md`
- the short descriptions of your skills

So the agent's memory between sessions is whatever you wrote down.

**Why it matters.** Change `CLAUDE.md` and the agent behaves differently, while the tools and skills stay exactly the same. Context is the brief that's already on the desk when someone walks into the office. If it's vague, every session starts vague.

**Try it yourself.** Add a line to your own `CLAUDE.md` (a tone, a rule, a unit you always use), start a new session, and see whether it holds. Then remove it.
