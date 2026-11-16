<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The LLM</p>

# An LLM reads and writes in pieces

<div data-widget="figure" data-name="tokens"></div>

> A **token** is a small piece of text: a whole word, part of a word, or a punctuation mark.

<!-- notes -->
**The idea.** An LLM doesn't see letters, or whole sentences, the way you do. It first cuts text into **tokens**: short pieces. A common word like *house* is usually one token. A longer or rarer word, like *fenestration*, is cut into several. A comma is a token of its own. As a rough guide for English, a token is about three-quarters of a word. The cuts in the picture are only an illustration, because every model cuts text its own way.

Everything the LLM does happens in tokens. It reads your message as tokens, and it writes its answer as tokens. And there is only one thing it ever produces: **the next token**. The "?" at the end of the first row is that.

**Why it matters.** It explains oddities you may have noticed. Counting the letters in a long word, or the digits in a long number, is awkward for an LLM, because it never sees the letters: it sees pieces. Token counts are also how the length of a conversation, and its cost, are measured.

**Try it yourself.** In Chat, ask how many letters are in a long, rare word (*fenestration*, say), and count them yourself. Notice whether the answer comes with the same confidence either way.
