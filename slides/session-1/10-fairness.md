<!-- layout: stage | where: chat -->
<p class="kicker">Part 1 · The LLM</p>

# Can an LLM be fair?

> In the Chat tab, start a **new conversation** and ask: **"Six of us need a presentation order. Pick who goes first, fairly: Aalto, Bo Bardi, Hadid, Kahn, Mies, Siza. Just the name."** Call out the name.

<div data-widget="llm-vs-tool" data-options="Aalto,Bo Bardi,Hadid,Kahn,Mies,Siza"></div>

<!-- notes -->
**The idea.** "Fair" here means each of the six has the same chance of going first. Each of you asked in a separate conversation, so the room's answers are like asking the LLM over and over. If it were fair, every bar would sit near the dashed line.

Usually it isn't. An LLM does have a little randomness built in, which is why your answers weren't all the same. But that randomness is weighted toward the *likely* answers, and some answers are simply more likely: the first name on the list, the most famous one, or the one that "sounds" like a choice. So it leans.

The dice tool (you'll read it in the next section) rolled the same number of times as there were answers. Its bars aren't perfectly level either, because a small sample always wobbles. Roll it again and the tallest bar moves somewhere else. The LLM's lean stays put. **A wobble that changes each time is chance. A lean that comes back is a bias.**

**Why it matters.** Crit order, a design competition draw, a random sample of sites to survey: when fairness matters, you need something that is fair by construction, not by good intentions.

**Try it yourself.** Ask Chat the same question ten times in ten new conversations, and keep a tally.
