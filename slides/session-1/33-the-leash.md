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
How much an agent may do before checking with you is a setting, and you choose it. The diagram shows four levels. At level 1 it only suggests, and you do the work. At level 2 it asks before every action. At level 3 it runs what you've already approved and asks about the rest. At level 4 it acts without asking. The app enforces the level. The model can only ask.

The Code tab's permission settings map roughly onto these levels. The course kits sit at level 3. Each kit's `.claude/settings.json` pre-approves `uv run tools/...`, so the course tools run without a prompt, while anything else, like deleting a file, asks first. Every permission prompt you've seen in your own folder today came from that setting.

Each level up is faster and leaves more for you to check afterwards. The right level depends on what a mistake costs. Renaming files in a scratch folder is cheap to undo, but overwriting last week's renders or emailing a client isn't. That is why the four items on the slide get different answers.

In your folder, ask Claude to do something the kits don't pre-approve, such as creating a new text file. Before you answer the prompt, read exactly what it is asking you to allow.
