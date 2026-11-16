<!-- layout: split | where: code-yours -->
<p class="kicker">Part 1 · The agent</p>

# An agent stops when it thinks it's done

<div class="cols" markdown="1">
<div markdown="1">

**A · "Done" can be checked**

> In the Code tab: **"Roll a six-sided die until the total passes 30. Show each roll."**

</div>
<div markdown="1">

**B · "Done" is a feeling**

> In the Code tab: **"Roll the dice until you get a good result."**

</div>
</div>

Run both. Then open the list of commands each one ran, and compare it with what the agent *told* you it did.

<div data-widget="figure" data-name="finish-line"></div>

<!-- notes -->
**The idea.** The loop needs a way to end. In **A** the end is written into the request: a running total, and a line it has to cross. A tool can add up the rolls, so the agent can check for itself, and so can you. In **B** nobody said what "good" means. The agent either asks you, or quietly picks a meaning of its own (a six? a double?) and stops when it gets one. Either way, the stopping point came from somewhere other than you.

**Why it matters.** Agents work best where "done" can be *measured*. "Make the stair comply with the code" can be checked by a tool. "Make the stair feel generous" can't, so the agent will stop when *it* feels done, and its feeling may not be yours. This is why later in the course you'll build tools that measure: they give the loop something solid to stop on.

**Trust the receipt.** After each run, open the commands it ran (in the Code tab, expand the tool calls). Does the story it told you match what it did? Sometimes an agent writes "I rolled a 4" without running anything. The commands are the record; the summary is just more generated text, like the explanation you saw in the LLM section.

**Try it yourself.** Rewrite B so that "good" can be checked, for example "a total of exactly 7 on two dice". Notice how much more you had to decide before the agent could.
