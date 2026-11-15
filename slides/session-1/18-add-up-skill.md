<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · The skill</p>

# A skill is know-how, written as text

<div data-widget="skill" data-path="kits/add/.claude/skills/add-up/SKILL.md" data-title=".claude/skills/add-up/SKILL.md"></div>

> Demo, in the Code tab: `/add-up` with **the same long sum you gave Chat**. Compare the two answers. Then ask it for 2 + 2.

<!-- notes -->
**The idea.** A **skill** is a text file that tells the agent how to approach one kind of task. On its own, a skill can't add anything up. What it can do is say *when* to use the tool that can, and *how*.

Click each part of the file:

- The **name and description** at the top are all Claude sees at the start of a session. It uses them to decide when the skill fits.
- The **steps** are a small **workflow**: the order the work should go in.
- The **rules** are what it must always or never do.

There's no code in it. You could have written it.

**The demo.** It was the same question you asked in Chat. This time you could see how the answer was made: the skill made Claude run the add tool, and the command was right there to read. Same LLM. The difference is a text file of under twenty lines.

**Why it matters.** "Never add in your head, not even 2 + 2" sounds fussy. But it's a choice about risk: how much does a wrong total cost you, compared with a few seconds of checking? Writing that choice down, once, is authorship. It's like the line in a practice's office manual that says every area schedule gets checked.

**Try it yourself.** Once you have the kit (in *Your turn*), give `/add-up` a list with mixed units, such as m² and ft². Does it follow the rule and ask first?
