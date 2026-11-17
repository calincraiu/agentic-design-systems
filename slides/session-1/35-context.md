<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · Context</p>

# Context is what the agent has in front of it

<div data-widget="context"></div>

> In your folder: add *"Announce every dice result like an excited sports commentator"* to your `CLAUDE.md`, start a **new session** and roll. Then take the line out again.

<!-- notes -->
**The idea.** **Context** is everything the agent knows while it works: your project instructions, the files it has read, and the conversation so far. Step through the widget and watch what is there at each moment.

The important step is the last one. When you start a **new session**, the conversation, the skill's full text and the tool's answers are gone. Of everything *you* wrote, only two things come back every time:

- your `CLAUDE.md`
- the short descriptions of your skills

So the agent's memory between sessions is whatever you wrote down.

One more thing is always there, and you didn't write it: the **app's own instructions**, including the list of tools the model can ask for. You can't see them or change them, but they're on the desk too.

**Why it matters.** Change `CLAUDE.md` and the agent behaves differently, while the tools and skills stay exactly the same. Context is the brief that's already on the desk when someone walks into the office. If it's vague, every session starts vague.

**The desk has a size.** The app sends the whole conversation to the model every time, and only so much fits. In a very long session, the app has to shorten what's there, and early details can blur. A new session with a good `CLAUDE.md` is often the cleaner start.

**Try it yourself.** Add a line you'd actually want to your `CLAUDE.md` (a tone, a rule, a unit you always use), start a new session, and see whether it holds.
