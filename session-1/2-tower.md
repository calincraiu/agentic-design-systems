# Part 2: A tower, and a difficult client

Same ideas, more interesting tool. [tools/tower.py](../tools/tower.py) builds a tower from eight numbers, measures it and draws it. Clients don't talk in eight numbers. Getting from one to the other is the design problem.

Work in pairs: one of you drives, and the other plays the client.

## 1. Meet the tool

Type:

> Build me a tower with the tower tool, using any numbers you like. Then show me what the tool can do, using its help.

Click `runs/gallery.html` in Claude's reply to open the gallery.

Then ask Claude to build **exactly the same tower again**, and compare the numbers. Unlike a die, this tool gives the same result for the same input every time. That's why you can trust it for measuring.

## 2. Take on a client

1. Choose a client card from [clients/](clients/). Two pairs should take the same card.
2. Type `/tower-designer` and name your card. Stop when Claude pauses with its questions.
3. **Read the brief** it wrote in `my-work/`. For each interpretation: do you agree? Edit what you don't. It's your brief.
4. The other person now plays the client, and answers the questions **in character**. Make things up if needed, but stay consistent.
5. Let Claude finish: three variants, a comparison and a recommendation.
6. Open the gallery. **Choose one direction yourselves.** Claude's recommendation is only an opinion.

Then find the pair with the same card and compare briefs. **Where did you read the same words differently, and how did that change the towers?**

## 3. Write a design stance

The tower designer's stance is "Balanced". Yours won't be.

1. Choose a stance and name it. For example:
   - *Good Neighbour*: the city comes first
   - *Sculptor*: form and silhouette lead
   - *Spreadsheet*: efficiency, always
   - *Storyteller*: the client's words, taken literally
   - or your own
2. Ask Claude to copy `.claude/skills/tower-designer/` to `.claude/skills/tower-<your-stance>/`, and to change the name and description.
3. Rewrite the **Design stance** section yourselves. Leave the workflow alone. Say what your stance values, what it refuses, and how its three variants differ.
4. **Start a new session**, then run your skill on **the same card**, reusing your brief.
5. Open the gallery and compare the runs of both skills under your client.

**You're done when** the gallery shows runs from both skills for the same client.

## Crit

Show your gallery and answer two questions:
1. What did your stance change?
2. What could your stance **not** change, however you wrote it?

The second answer is where Session 2 begins.
