<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The LLM</p>

# It writes one piece at a time, and reads it all again

<div data-widget="figure" data-name="token-loop"></div>

> Each piece is a **token**: a whole word, part of a word, or a punctuation mark. Once a piece is written, it stays: every next piece builds on it.

<!-- notes -->
An LLM doesn't read letters or whole sentences. It splits text into **tokens**. A common word like *house* is usually one token, a rarer one like *fenestration* is split into several, and punctuation marks are tokens of their own. In English, a token averages about three-quarters of a word.

It writes by repeating one step. It reads everything so far (your message and whatever it has already written), chooses a likely next token, adds it to the end, and then repeats with the slightly longer text until the answer is complete. The technical term is **autoregressive**.

A few consequences:

- It can't take a token back. Everything after a token builds on it, so an odd choice early on can steer the rest of the answer while the tone stays confident.
- It never sees the individual letters of a long word or the digits of a long number, only the tokens. That makes counting letters and doing long arithmetic harder for it than they look.
- The length of a conversation, usage limits and cost are all measured in tokens.

The same read, add, repeat pattern comes back in the agent section, one level up.

In three new conversations, ask: "Write one sentence about a tower, starting with *The tower*." Find the first word where the answers differ. From there, each answer continues from its own choice, so they drift further apart.
