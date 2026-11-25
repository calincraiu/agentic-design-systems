<!-- layout: diagram | where: app -->
<p class="kicker">By the end of today</p>

# Three things you'll be able to do

<div data-widget="figure" data-name="outcomes" data-start="1"></div>

<!-- notes -->
The first is a tool made from a Grasshopper definition. You name its inputs and outputs and write its contract. Claude then sends values for the inputs, the definition runs in Rhino, and Claude reads the outputs back, the way it ran `add.py` in Session 1, leaving a receipt in `runs/`. Any definition can become a tool this way. You build the smallest one, adding two numbers, in Part 1.

The second is a measure on a real site. The site file holds a plot, a park, a river and neighbouring blocks. A measure takes a tower Claude has built and returns one number about it, such as the share of the park's sun the tower takes away.

The third is a skill you write, `tower-check`. It runs your measures and compares each result with a limit you choose. The measures are exact; the limits are judgements, and writing the reason for each one is part of the task.

The numbers in the figure are examples.
