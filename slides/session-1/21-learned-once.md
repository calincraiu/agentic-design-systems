<!-- layout: diagram | where: chat -->
<p class="kicker">Part 1 · The LLM</p>

# It learned once, then stopped.

<div data-widget="figure" data-name="frozen"></div>

> In Chat, a new conversation: **"Who won the most recent Pritzker Prize, and what is today's date?"** Did it search the web, or answer from memory? How can you tell?

<!-- notes -->
The model's sense of what is likely comes from **training**. Before release it is shown a huge body of text many times over, and its numbers are adjusted each time so that it predicts the next token a little better. It is then trained further to follow instructions and hold a conversation. After that the numbers are **frozen**, so the model doesn't change while you use it. That has three consequences.

- **It has a cutoff date** and knows nothing that happened after it. It may not know today's date unless the app tells it.
- **It doesn't look things up.** It has no database of facts. If the app gives it web search, you'll see that it searched and which pages it opened. Open one of them, because the summary can still misquote it. If no search is shown, the answer came from training.
- **It doesn't learn from you.** Apps with a "memory" feature save notes and put them in front of the model in later conversations, as text. The model itself stays the same.

Building regulations, product data, a site's planning history, a brief the client changed yesterday: none of it can be relied on to be in the model. The only way to give it new information is to put the text in front of it. That is **context**, the last part of Part 1, and your `CLAUDE.md` is already an example.

Ask about something in your field that changed recently, such as a new regulation or a competition result. Then paste in the source and ask again.
