<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · The agent</p>

# Nobody wrote the plan.

> **Guess first:** how many rolls will it take to get a double (the same number on both dice)? Call out your number.
>
> Then, in the Code tab with your folder open: **"Roll two dice until you get a double. Tell me how many tries it took."** Call out the answer. Ask it again.

<div data-widget="tries"></div>

<!-- notes -->
**The idea.** This is the loop from the last slide, running in your own folder. An **agent** is an LLM that can use tools and decide what to do next. It reads files, runs tools, looks at the results and tries again, within the limits you set.

**Your guess.** A double turns up on one roll in six, so the *average* is six rolls. But an average hides a lot: one run might take 1 roll, the next 20. The two charts put the room's guesses next to the room's real runs. Most people guess 2 or 3. If yours was low, that is normal: we expect chance to even out faster than it does.

Nobody said how many times to roll, or when to stop. Claude worked that out by itself, reading each result as it came back: roll, check for a double, roll again, stop. **Run it a second time and it usually takes a different number of steps** (about one pair of runs in eleven matches by chance). The plan wasn't written in advance; each step depended on the last result. A recipe always has the same steps. An agent's steps depend on what it sees. That loop of acting, looking and deciding is what makes it an agent.

Sometimes Claude writes a little program that rolls in a loop instead of calling the tool again and again. That's still the agent deciding *how* to do the job.

**Why it matters.** Most design work is iterative: try, look, adjust. An agent can run that loop quickly, but it is still an LLM deciding what is good enough to stop at. That's why you set the goal and the limits, and why you check what comes back.

**Try it yourself.** Ask the same thing three more times and write down the tries each time. How far apart are your numbers? Then open the commands it ran for one of them, and count the rolls yourself.
