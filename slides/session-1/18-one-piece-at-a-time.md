<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The LLM</p>

# It writes one piece at a time, and reads it all again

<div data-widget="figure" data-name="token-loop"></div>

> Each piece is a **token**: a whole word, part of a word, or a punctuation mark. Once a piece is written, it stays: every next piece builds on it.

<!-- notes -->
**The idea.** An LLM doesn't see letters, or whole sentences, the way you do. It cuts text into **tokens**: short pieces. A common word like *house* is usually one token. A longer or rarer word, like *fenestration*, is cut into several. A comma is a token of its own. As a rough guide for English, a token is about three-quarters of a word.

It writes by repeating one small step. It reads *everything* so far (your message, plus whatever it has already written), chooses one likely next token, and adds it to the end. Then it does the same again, reading the slightly longer text, until the answer is finished. The technical name for this is **autoregressive**: each piece depends on the pieces before it, even the ones it wrote a moment ago.

**Why it matters.** Three things follow.

- **It can't take a piece back.** Whatever it weighs up internally, once a piece is written, everything after it builds on it. An early odd choice shapes the rest, which is how an answer can drift off while sounding sure of itself.
- **An explanation is written the same way.** When you ask how it worked something out, that answer is generated piece by piece too. It isn't read from a record of what happened.
- **Letters and digits are awkward for it.** It never sees the letters in a long word, or the digits in a long number, only the pieces. Token counts are also how the length of a conversation, and its cost, are measured.

Keep the shape in mind: *look at what is there, add one thing, go round again.* It comes back when you meet the agent.

**Try it yourself.** In three fresh chats, ask the same thing: "Write one sentence about a tower, starting with *The tower*." Find the word where the three answers first differ. After that point, each answer builds on its own choice, so they drift apart.
