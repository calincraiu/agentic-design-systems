<!-- layout: diagram | where: app -->
<p class="kicker">What answered you?</p>

# The model is far away. Your files are here.

<div data-widget="figure" data-name="where-it-runs"></div>

> Whatever the model reads leaves your laptop: text, images, files.

<!-- notes -->
The model is far too large to run on a laptop, so it runs in a **data centre** belonging to the company that makes it. The app, your folder and the tools are on your laptop.

Each time you send a message, the app sends the model everything it needs to read: your message, the conversation so far, your `CLAUDE.md`, any file or image Claude has opened, and anything the tools printed. The model sends text back. Anything that *happens* on your computer, such as a file being saved or a tool running, is done by the app. One exception is worth knowing. When the Chat tab runs code, it does so on the provider's computers. Only the Code tab runs things on your laptop.

Three practical consequences:

- **Confidentiality.** If Claude opens a file, its contents go to the provider. That includes client drawings, a competition entry under embargo or a fee proposal. Check the AI policy of your school, your practice and your client before using project files with any AI app.
- **No internet, no model.** The app still opens and the tools still run, but nothing can answer.
- **Limits and cost** are counted in the amount of text sent back and forth.

Think of a file from a current project that you wouldn't email to a stranger, and what you would need to check before opening it with Claude.
