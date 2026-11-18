<!-- layout: split | where: app -->
<p class="kicker">Part 1 · The tool</p>

# Some answers can't be known in advance

<div class="cols" markdown="1">
<div markdown="1">

<div data-widget="dice"></div>

> The add tool must give the **same** answer every time. The dice tool must **not**. Roll twice and compare.

</div>
<div data-widget="file" data-path="kits/dice/tools/dice.py" data-highlight="17" data-title="tools/dice.py: the whole tool"></div>
</div>

<!-- notes -->
**The idea.** The dice tool has the same shape as the add tool: inputs at the top (`--sides`, `--count`), one line that does the work (highlighted), and the output at the bottom. These inputs have *names*. `--sides 6` reads as "sides: 6", so the order doesn't matter.

The difference is the job. The add tool must give the same answer every time. The dice tool must *not*. Both are promises, and both are kept exactly.

**Why it matters.** When you design a tool later in the course, you'll decide what kind of promise it makes. "Always the same answer for the same inputs" is what you want for measuring. "Fair, every time" is what you want for choices, and for sampling variations.

**Try it yourself.** In Chat, ask: "Roll a six-sided die 20 times. Just the numbers." Count how often the same number comes up **twice in a row**. Then roll 20 with the tool and count again. In 20 real rolls, a repeat turns up about three times on average. Chat's "random" lists often have fewer: they look *too* even, because a list that looks random is not the same as one that is. People do the same when asked to make up random numbers. Real chance is lumpier than it looks. (If Chat ran code to roll, it reached for a tool.)
