<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The agent</p>

# The model asks. The app acts.

<div data-widget="figure" data-name="request-run"></div>

> The model never touches your folder. It writes a request, and the **app** runs it, if you've allowed it.

<!-- notes -->
**The idea.** The model only writes text, and it runs far away. So how does an agent roll a die on *your* laptop? Each time it "acts", four things happen:

1. **The model writes a request**, in a fixed format: which tool, and which inputs.
2. **The app reads it and checks the leash.** Is this allowed already? If not, it asks you.
3. **The app runs the tool** on your laptop.
4. **The app pastes the tool's output back in, as text.** The model reads it and writes its next piece. That's the "look" in the loop.

Every round of the agent's loop is these four steps.

**Why it matters.** It explains three things you'll meet in the next few slides:

- **The receipt** is written by the app as it runs each command, not by the model. That's why you can trust it: it's a record, not a description. It proves what ran and what came back, not that the summary the model writes afterwards is right, so compare the two.
- **Permission prompts** come from the app. The model can't skip them, only ask.
- **"I rolled a 4."** If the model writes a sentence instead of a request, nothing runs. There's no command behind it, and no receipt. It's just text.

**Try it yourself.** In the next run, expand a tool call in the Code tab. The command is the model's request. The text under it is what the app pasted back.
