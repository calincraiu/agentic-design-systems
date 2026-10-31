# Part 1: The smallest possible system

A die is about as simple as a tool can get. That leaves your attention free for the ideas: what is an LLM, a tool, an agent, a skill and context, and how do you tell them apart?

Work in pairs. Definitions are in [concepts.md](concepts.md).

## 1. An LLM on its own

In the **Chat** tab, type:

> Pick a random number from 1 to 20.

Write your answer on the board with everyone else's. Look at the board. Is that what random looks like?

An LLM (large language model, the AI itself) produces text that fits. It writes something that *looks like* a random number. Nothing was rolled.

## 2. A tool

Go to the **Code** tab, in this folder, and type:

> Roll two dice using the dice tool.

Now open [tools/dice.py](../tools/dice.py) and read it. It's short enough to read in full. Look for:
- what goes in (`--sides`, `--count`)
- the line where the roll actually happens
- what comes out

A **tool** really does the thing. Its inputs and outputs are written down, and you can read how it works.

## 3. An agent

Type:

> Roll two dice until you get a double. Tell me how many tries it took.

Watch what happens. You didn't say how many times to run the tool, or when to stop. Claude worked that out, reading each result as it went.

An **agent** is an LLM that can use tools and decide what to do next.

## 4. A skill

Type `/tie-breaker`, and settle something real: where should you two eat lunch?

Now open [.claude/skills/tie-breaker/SKILL.md](../.claude/skills/tie-breaker/SKILL.md). There's no code in it. It's a page of instructions, and you could have written it.

A **skill** is reusable know-how. The steps in it are a small **workflow**. Try to break it: ask for a re-roll, or ask Claude which option it would pick.

## 5. Context

Open [CLAUDE.md](../CLAUDE.md) and add this line at the very end:

> Announce every dice result like an excited sports commentator.

Save it, **start a new session** in the Code tab, and ask for a roll.

The tool didn't change, and neither did the skill. **Context** is what the agent knows before you ask for anything, and `CLAUDE.md` is loaded at the start of every session.

Delete the line again when you've seen it work.

## 6. Write your own skill

Now write a skill of your own that uses the dice. For example:
- *Crit order:* who presents first?
- *Random client:* roll to build a client from a list of who, what and where
- *Board game referee:* for a game you've just invented

Steps:
1. Decide what the skill should do, and what it must never do.
2. Ask Claude to create a new skill in `.claude/skills/`, using `tie-breaker` as the starting point. Then edit the text until it says what *you* mean. This writing is the part to do yourselves.
3. **Start a new session**, so that Claude sees the new skill.
4. Run it, and adjust the text if it doesn't behave.

**You're done when** your skill works, and you can answer this: **what can your skill not make the tool do?** Try asking your skill for a 7 on a six-sided die. Keep your answer in mind for Part 2.
