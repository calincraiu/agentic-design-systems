<!-- layout: stage | where: code-yours -->
<p class="kicker">Part 1 · The skill</p>

# A skill is know-how, written as text

<div data-widget="skill" data-path="kits/add/.claude/skills/add-up/SKILL.md" data-title=".claude/skills/add-up/SKILL.md"></div>

> In the Code tab, in your folder: `/add-up` with **the same long sum you gave Chat**. Compare the two answers, and check the receipt. Then ask it for 2 + 2.

<!-- notes -->
A skill can't do anything by itself. It tells the agent when to use the tool that can, and how. Click through the parts of the file:

- The **name and description** at the top are the only part Claude sees at the start of a session. It uses them to decide whether the skill fits a request.
- The **steps** are a short **workflow**, the order the work should go in.
- The **rules** are what it must always or never do.

It's plain English, with no code in it.

You gave the same sum to Chat earlier. This time the skill had Claude run the add tool, and the command and its output are there to read. The model is the same. What changed is a text file of eighteen lines.

"Never add in your head, not even 2 + 2" can look excessive. It's a judgement about risk, weighing what a wrong total would cost against the few seconds it takes to run a tool. A practice's office manual makes the same kind of call when it says every area schedule gets checked.

Give `/add-up` a list that mixes m² and ft², and see whether it follows its rule and asks before adding.
