<!-- layout: diagram | where: app -->
<p class="kicker">What answered you?</p>

# One model, many apps

<div data-widget="figure" data-name="model-app"></div>

> The **model** writes. The **app** decides what the model is given, and what it can reach.

<!-- notes -->
The model is the part that reads and writes text. It runs on Anthropic's servers and comes in several versions (Opus, Sonnet, Haiku) that you can choose between in the app.

You never use the model directly. You use an **app**, a program that sends your text to the model over the internet and shows you what comes back. The same model sits behind all of them:

- the **web app**, in a browser
- the **desktop app**, installed on your computer. Its Chat and Code tabs behave like two separate apps, each giving the model its own hidden instructions, its own tools and its own permissions.
- an **add-in**, a panel inside another program that passes your words to the model

In this course "the app" means that surrounding program and what it gives the model. Other companies are built the same way. ChatGPT, for example, is OpenAI's app around its GPT models.

Everything you write in this course lives on the app's side: your `CLAUDE.md`, your skills, your tools, your permissions. You never change the model itself, which is also why the same ideas carry over to other apps. Models also get replaced over time. A tool will give the same answer next year; a newer model may not.

To see the two halves separately, ask Chat the same question twice with a different model picked each time (same app, different model). Later today, ask it in the Code tab (same model, different app).
