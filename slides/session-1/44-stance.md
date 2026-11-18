<!-- layout: task | where: code-yours | time: 20 min | pairs -->
<p class="kicker">Your turn</p>

# Give it a point of view

1. **Agree** with your partner how you'll answer the agent's three questions. Write the answers down: you both give the same ones.
2. **Each pick** a different stance below.
3. In your folder, open `.claude/skills/tower-designer/SKILL.md` and replace the *Balanced* paragraph under *Design stance* with **three sentences** of your own.
4. In a **new session**, run `/tower-designer` with **the wish you gave Chat at the start**.

- *Good Neighbour*: the smallest shadow wins
- *Sculptor*: silhouette first, every variant twists or leans
- *Spreadsheet*: the most floor area, no overhangs
- *Storyteller*: take every word literally

> **You're done when** your two galleries differ, and you can point to the sentence that made the difference.

<!-- notes -->
A **design stance** says what a skill values. The tower designer's stance is *Balanced*, meaning it has no strong views. Yours should have some. Your three sentences say what it values most, what it refuses, and how its three variants should differ. Leave the workflow alone: the questions, the brief and the report stay as they are.

The task is an experiment with one variable. You and your partner use the same wish, the same answers, the same tool and the same workflow. Only the stance differs, so any difference between your towers comes from those three sentences. If you answered the questions differently, you couldn't tell whether the stance or the answers made the difference.

You edit the skill in place, as you did on the *Change one rule* slide. The original *Balanced* text is still in the course folder, in `kits/tower`.

While it runs:

- If it asks something you didn't agree on, decide the answer together and both give it.
- Read the brief in `briefs/`. It should be almost the same as your partner's.
- Open `runs/gallery.html` and compare the metrics table with your partner's: shadow, floor area, cantilever.

Put your stance in a skill of its own, so you keep both. Ask Claude to copy `tower-designer` to `tower-<your-stance>` and check that the `name:` line changed too. If it didn't, the gallery labels your runs `tower-designer`.
