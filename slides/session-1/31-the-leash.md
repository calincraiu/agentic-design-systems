<!-- layout: split | where: app -->
<p class="kicker">Part 1 · The agent</p>

# You set the leash

<div class="cols" markdown="1">
<div markdown="1">

**Hands up: would you let it do this without asking?**

- Rename the files in your project folder
- Overwrite last week's renders
- Start a four-hour job
- Email the client

</div>
<div data-widget="figure" data-name="leash" data-start="0" data-ghost></div>
</div>

<!-- notes -->
**The idea.** How much an agent may do before it checks with you is a setting, and *you* choose it. There are four broad levels. At one end it only suggests. At the other it acts with no questions. Between them, it can ask before every action, or run what you've already approved and ask about the rest. The leash is held by the **app**, not the model: the model can only ask.

**Why it matters.** Each step up is faster, and each step up means more for you to check afterwards. The right level depends on what a mistake costs. Renaming files in a scratch folder is cheap to undo. Overwriting last week's renders or emailing a client is not. Hands went up at different places because the *cost of being wrong* is different for each item, not because anyone is more or less careful.

The course kits start on level 3. They pre-approve running the course's own tools (`uv run tools/...`). That is why those commands run without asking, while anything else, like deleting a file, stops and asks. When a permission prompt appears, you are using the leash.

You've already met the leash: every permission prompt in your own folder today was level 3 at work.

**Try it yourself.** In your own folder, ask Claude to do something outside the pre-approved tools, like making a new text file. Read the prompt before you answer it. What exactly is it asking you to allow?
