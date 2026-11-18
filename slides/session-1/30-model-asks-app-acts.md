<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The agent</p>

# The model asks. The app acts.

<div data-widget="figure" data-name="request-run"></div>

> The model never touches your folder. It writes a request, and the **app** runs it, if you've allowed it.

<!-- notes -->
The model only produces text, and it runs in a data centre. For an agent to roll a die on your laptop, each action goes through four steps:

1. **The model writes a request** in a fixed format, naming the tool and the inputs.
2. **The app checks whether that request is allowed.** If it isn't allowed already, the app asks you.
3. **The app runs the tool** on your laptop.
4. **The app adds the tool's output to the conversation**, as text. The model reads it and writes its next piece. This is the "look" step of the loop.

Every round of the agent's loop is these four steps.

This explains several things in the next few slides. The receipt (the list of commands and what they printed) is written by the app as it runs them, not by the model, so it is a record rather than a description. It shows what ran and what came back. It doesn't prove that the model's summary afterwards is right, so compare the two. Permission prompts also come from the app, so the model can't skip them. And if the model writes "I rolled a 4" as an ordinary sentence instead of a request, nothing runs and there is no receipt for it.

In your next run in the Code tab, expand a tool call. The command is the model's request, and the text below it is what the app passed back.
