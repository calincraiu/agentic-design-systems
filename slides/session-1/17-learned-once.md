<!-- layout: diagram | where: chat -->
<p class="kicker">Part 1 · The LLM</p>

# It learned once, then stopped.

<div data-widget="figure" data-name="frozen"></div>

> In Chat, a new conversation: **"Who won the most recent Pritzker Prize, and what is today's date?"** Did it search the web, or answer from memory? How can you tell?

<!-- notes -->
**The idea.** Where does "likely" come from? From **training**. Before release, the model is shown a huge library of text, over and over, and its numbers are adjusted each time so that it predicts the next piece a little better. It's then trained further to follow instructions and hold a conversation. Then the numbers are **frozen**. The model you talk to doesn't change while you use it. Three things follow:

- **It has a cutoff date.** It knows nothing that happened after its training. It may not even know today's date unless the app tells it.
- **It doesn't look things up.** It has no database of facts. If the app gives it a web search, the app shows that it searched and which pages it opened: that's a receipt. Facts and quotes in the answer can still be wrong, so open one of the pages. If not, the answer came from what's likely.
- **It doesn't learn from you.** Nothing you say changes the model. Apps with a "memory" feature save notes and put them back in front of the model next time, as text.

**Why it matters.** Building regulations, product data, a site's planning history, the brief your client changed yesterday: none of it is reliably *in* the model. The only way to give it something new is to put the text in front of it. That's what **context** is, and you'll meet it at the end of Part 1. Your `CLAUDE.md` is the first piece.

**Try it yourself.** Ask about something in your field that changed recently, such as a new regulation or a competition result. Then paste in the source and ask again. Compare the two answers.
