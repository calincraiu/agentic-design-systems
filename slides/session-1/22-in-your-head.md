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
You don't calculate 2 + 2; you remember it. For two thirteen-digit numbers there's nothing to remember, so you would use paper or a calculator.

An LLM is in a similar position. It has seen 2 + 2 = 4 countless times. For long numbers it writes the digits that seem likely to come next, which is often right and sometimes off by a digit or two. Newer models are much better at this, and some run a small calculation behind the scenes. Either way, the number on its own doesn't show how it was produced.

The third question is the important one. The explanation you get ("first I add the cents, carry the one…") is more generated text, written after the answer. It describes a plausible method, not what actually happened. Researchers at Anthropic tested this by looking inside a model while it added 36 + 59. The model described the carrying method taught at school, while internally it had done something different, combining a rough estimate of the total with an exact last digit. (Anthropic, "Tracing the thoughts of a large language model", March 2025.) If Chat showed you code that it ran, that's a different case: it used a tool.

Some apps show the model "thinking" before it answers. That is also generated text, written first, one token at a time. It often improves the answer, much as working on paper helps you, but it isn't a record of a calculation.

This is where the course's main habit comes from: **check the receipt**. An explanation is text. A **receipt** is the record of what actually ran, meaning the exact command and what the tool printed back. "Behind the scenes" under the widget shows the receipt for this sum. Area schedules, cost plans and unit counts need a receipt.

Ask Chat to add twenty room areas with two decimals each. Later, check its total with `/add-up` in your own folder.
