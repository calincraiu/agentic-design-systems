<!-- layout: split | where: code-yours -->
<p class="kicker">Part 1 · The agent</p>

# An agent stops when it thinks it's done

<div class="cols" markdown="1">
<div markdown="1">

**A · "Done" can be checked**

> In the Code tab: **"Use the dice tool to roll a six-sided die until the total passes 30. Keep the running total with the add tool. Show each roll."**

</div>
<div markdown="1">

**B · "Done" is a feeling**

> In the Code tab: **"Use the dice tool to roll until you get a good result."**

</div>
</div>

Run both. Then **check the receipt**: every roll should be a `dice.py` command. Open the list of commands each one ran, and compare it with what the agent *told* you it did.

<div data-widget="figure" data-name="finish-line"></div>

<!-- notes -->
**The idea.** The loop needs a way to end. Both requests name the same tool, so the only difference is the finish line. In **A** the end is written into the request: a running total, and a line it has to cross. The add tool keeps that total exact, so the number isn't the LLM's own arithmetic. The agent still decides when it has passed 30, but now you can check that decision. In **B** nobody said what "good" means. The agent either asks you, or quietly picks a meaning of its own (a six? a double?) and stops when it gets one. Either way, the stopping point came from somewhere other than you.

**Why it matters.** Agents work best where "done" can be *measured*. "Make the stair comply with the code" can be checked by a tool. "Make the stair feel generous" can't, so the agent will stop when *it* feels done, and its feeling may not be yours. This is why later in the course you'll build tools that measure: they give the loop something solid to stop on.

**Check the receipt.** After each run, open the commands it ran (in the Code tab, expand the tool calls). You asked for the tools by name, so every roll should be a `uv run tools/dice.py` command, and in A every new total an `add.py` command. Count them against the rolls in its summary. Sometimes an agent writes "I rolled a 4" without running anything, even when told to use the tool: the model wrote a sentence, not a request, so the app had nothing to run. The commands are the record; the summary is just more generated text, like the explanation you saw in the LLM section.

**Try it yourself.** Rewrite B so that "good" can be checked, for example "a total of exactly 7 on two dice". Notice how much more you had to decide before the agent could. Then try A *without* naming the tools: does it still use them, or does it roll and add in its head? In a few slides you'll meet **skills**, which write "always use the tool" down once so you don't have to say it every time.
