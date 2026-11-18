<!-- layout: task | where: code-yours | time: 10 min | pairs -->
<p class="kicker">Part 1 · The skill · your turn</p>

# Change one rule

1. Open **your copy** of `add-up` or `tie-breaker`, in `.claude/skills/` in your folder.
2. Change or add **one rule**, in your own words.
3. Start a **new session**, run the skill, and see what changed.
4. Ask it for a **7 on a six-sided die**.

- *add-up*: compare the total with a target area
- *add-up*: give every total in m² and ft²
- *tie-breaker*: put everyone in order, not just first
- *tie-breaker*: allow one re-roll, if everyone agrees

> **You're done when** the behaviour changed the way you meant, and you can answer: **what can your rule not make the tool do?**

<!-- notes -->
A skill is plain text, so changing what the agent does can be a one-sentence edit. You can ask Claude to make the change or type it yourself in a text editor. Either way, read the result, since the wording is your responsibility.

Claude Code picks up the edit straight away, but if the skill already ran in this conversation, its old text is still in the context. Start a **new session** so only the new version is there.

The 7 is the part to pay attention to. The dice tool can't roll a 7 on a six-sided die, but the model can still write "I rolled a 7", since writing it takes no tool. A rule against it in the skill or in your `CLAUDE.md` makes that less likely. Only the tool's output shows what was actually rolled.

That points to three kinds of rule, which behave differently:

- A rule in a skill or in `CLAUDE.md` is text the model *reads*. It is usually followed, but never guaranteed.
- A permission is *enforced* by the app. The model can't get past it.
- A tool is *exact*, but only when it is used, and whether it gets used depends on a rule of the first kind. The receipt shows whether it ran.

When a rule matters, work out which kind it is.

If your change seems to have no effect, start a new session, and check that you edited the copy in your own folder rather than the one in the course folder.

For more practice, write a new skill that uses the tools you have: a *crit order* (everyone, in a fair order), an *area check* (add up rooms and compare the total with a target), a *random client* built from rolled lists, or a *board game referee*. Ask Claude to create a new folder in `.claude/skills/`, starting from `add-up` or `tie-breaker`, then rewrite the text until it says what you mean. Swap with your partner and try to find a request that makes their skill break its own rules.
