<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · The agent</p>

# Nobody wrote the plan.

> **Guess first:** how many rolls will it take to get a double (the same number on both dice)? Call out your number.
>
> Then, in the Code tab with your folder open: **"Roll two dice until you get a double. Tell me how many tries it took."** Call out the answer. Ask it again.

<div data-widget="tries"></div>

<!-- notes -->
This is the loop from the last two slides, running in your own folder. Nobody told Claude how many times to roll or when to stop. It rolled, checked for a double, and either rolled again or stopped, based on each result. Run it a second time and it usually takes a different number of steps. Two runs match by chance only about one time in eleven. A recipe has fixed steps, whereas here the steps depend on the results.

The guess is harder than it looks. A double comes up on one roll in six, so the average is six rolls, but individual runs vary a lot. About half finish within four rolls, and about one in six takes more than ten. Guesses tend to come in under six, because we expect chance to even out faster than it does.

Sometimes Claude writes a short program that rolls in a loop instead of calling the tool again and again. That is still the agent choosing how to do the job, and the receipt will show the program it ran.

Because the agent decides when the goal has been met, it's up to you to set the goal and the limits, and to check what comes back.

Run the request three more times and note the number of tries each time. Then open the commands for one run and count the rolls yourself.
