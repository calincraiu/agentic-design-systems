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
The dice tool has the same structure as the add tool: inputs at the top (`--sides`, `--count`), one line that does the work (highlighted), and the output at the bottom. Its inputs are named, so `--sides 6 --count 2` and `--count 2 --sides 6` mean the same thing.

The difference is what each tool guarantees. The add tool must give the same answer for the same inputs every time. The dice tool must not; each roll is meant to be unpredictable and fair. When you design a tool later in the course, you'll decide which kind of guarantee it makes. Repeatable output suits measuring. Fair randomness suits choosing, and sampling variations.

In Chat, ask "Roll a six-sided die 20 times. Just the numbers." and count how often the same number comes up twice in a row. Then do 20 rolls with the tool and count again. Twenty rolls give 19 neighbouring pairs, each with a 1 in 6 chance of matching, so you would expect about three repeats. Chat's lists often have fewer. People do the same when asked to invent random numbers, because real randomness has more runs and clumps than we expect. If Chat ran code to roll, it used a tool, and its result should look like the tool's.
