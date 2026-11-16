<!-- layout: stage | where: chat -->
<p class="kicker">Part 1 · The LLM</p>

# In your head, or on paper?

> In the Chat tab:
>
> 1. Ask **"What is 2 + 2?"**
> 2. Ask **"What is 8437209516384.27 + 6958173402659.86? Just the number."** Paste the answer below.
> 3. Ask **"How exactly did you work that out?"**

<div data-widget="add" data-poll data-numbers="8437209516384.27 6958173402659.86"></div>

<!-- notes -->
**The idea.** You don't calculate 2 + 2: you *remember* it. For two thirteen-digit numbers there's nothing to remember, so you'd reach for paper or a calculator.

An LLM is in the same position. For 2 + 2 it has seen the answer countless times. For long numbers it writes digits that are likely to come next, which often looks right and sometimes is. Newer models are much better at this, and some quietly run a calculation in their own space. Either way, the answer alone doesn't tell you *how* it was made.

**The third question is the surprise.** The explanation Chat gives you ("first I add the cents, carry the one…") is more generated text, written after the fact. It's a likely-sounding description of a method, not a record of what happened. When researchers at Anthropic looked inside Claude as it added 36 + 59, it described the carrying method from school, while internally it had done something quite different. If Chat ran code instead, you'll have seen the code. Then it reached for a tool, which is exactly the lesson.

**Why it matters.** Area schedules, cost plans, unit counts: architecture is full of totals that have to be *right*, not plausible. A colleague who calls out a total is not the same as one who hands you the calculation sheet. "Behind the scenes" under the widget is that sheet: the exact command, and the tool's raw answer.

**Try it yourself.** Ask Chat to add a column of twenty room areas with two decimals each. Check the total with the add tool once you have it in your folder.
