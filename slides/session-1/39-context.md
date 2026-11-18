<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · Context</p>

# Context is what the agent has in front of it

<div data-widget="context"></div>

> In your folder: add *"Announce every dice result like an excited sports commentator"* to your `CLAUDE.md`, start a **new session** and roll. Then take the line out again.

<!-- notes -->
**Context** is everything the model has to work with at a given moment: the app's instructions, your project instructions, the files it has read and the conversation so far. Step through the widget to see it build up.

The last step matters most. In a new session, the conversation, the full text of any skills used and the tools' outputs are all gone. Of what you wrote, two things are loaded every time:

- your `CLAUDE.md`
- the short descriptions of your skills

So between sessions, the agent only knows what you wrote down. The **app's own instructions**, including the list of tools the model can ask for, are also always there. You can't see or change them.

That is why the commentator line works. The tools and skills stay exactly the same, but one line in `CLAUDE.md` changes every session. A vague `CLAUDE.md` gives every session a vague start, the way a vague brief does for anyone joining a project.

Context also has a size limit. The app sends the whole conversation to the model on every turn, and only so much fits. In a very long session the app shortens older parts, and early details can get lost. A new session with a good `CLAUDE.md` is often the cleaner option.

Add a line you would actually want to your `CLAUDE.md` (a tone, a rule, units you always use), start a new session, and see whether it holds.
