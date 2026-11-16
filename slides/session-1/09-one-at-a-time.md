<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · The LLM</p>

# It adds one piece, then reads it all again

<div data-widget="figure" data-name="token-loop"></div>

> This is called **autoregressive**: each new piece is built on the ones before it, including the ones the LLM wrote itself.

<!-- notes -->
**The idea.** The LLM writes by repeating one small step. It reads *everything* so far (your message, plus whatever it has already written), chooses one next token, and adds it to the end. Then it does the same again, reading the slightly longer text. It repeats this until the answer is finished. The name for this is **autoregressive**: *auto* means itself, and *regressive* means looking back. Each piece depends on the pieces before it, even the ones it wrote a moment ago.

**Why it matters.** Two things follow. First, there is **no plan**. The LLM doesn't write a draft and then polish it: it commits to one piece at a time and builds on it. An early choice, even an odd one, shapes everything after it, which is how an answer can drift off while sounding sure of itself. Second, an explanation is written the same way as everything else. When you asked Chat how it worked out a sum, that answer was generated piece by piece too. It wasn't read from a record of what happened.

Keep the shape in mind: *look at what is there, add one thing, go round again.* It comes back when you meet the agent.

**Try it yourself.** In three fresh chats, ask the same thing: "Write one sentence about a tower, starting with *The tower*." Find the word where the three answers first differ. After that point, each answer builds on its own choice, so they drift apart.
