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
Both requests use the same tool. What differs is the finish line. In **A** it is written into the request as a running total and a value to pass. The add tool keeps the total exact, so it isn't the model's own arithmetic. The agent still decides when it has passed 30, but you can check that decision against the commands. In **B** nobody defined "good". The agent either asks you what you mean, or picks a meaning of its own (a six? a double?) and stops when it gets one. Either way, the stopping point didn't come from you.

Agents work best where "done" can be measured. "Make the stair comply with the regulations" can be checked by a tool. "Make the stair feel generous" can't, so the agent stops when it judges the job done, and its judgement may not match yours. That is why later sessions build tools that measure.

After each run, expand the tool calls. You named the tools, so every roll should be a `uv run tools/dice.py` command, and in A every new total an `add.py` command. Count them against the rolls in the summary. Occasionally an agent reports a roll with no command behind it, even when told to use the tool. The commands are the record, and the summary is generated text.

Rewrite B so that "good" can be checked, for example "a total of exactly 7 on two dice", and notice how much you had to decide first. Then run A without naming the tools and see whether it still uses them. The skill section shows how to write "always use the tool" down once instead of repeating it in every request.
