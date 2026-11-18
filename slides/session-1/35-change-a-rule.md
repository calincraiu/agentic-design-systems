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
**The idea.** A skill is plain text, so changing what the agent does can be as small as changing one sentence. You can ask Claude to make the edit, or open `SKILL.md` in a text editor and type it yourself. Either way, read the result: the words are your job. That's authorship.

Claude Code notices your edit straight away. But if the skill already ran in this conversation, its old text is still in the context, so start a **new session** to give the agent a clean desk with only your new version on it.

**The 7 is the important question.** The dice tool *can't* roll a 7 on a six-sided die. But the LLM can still *write* "I rolled a 7", because writing is all it needs to do that. A rule can tell it not to, and the rule in your `CLAUDE.md` helps. Only the tool guarantees what actually happened, though. That's why the tool's output, not the agent's description of it, is the evidence: check the receipt.

**Soft rules and hard rules.** Your rule is text the model *reads*: it's usually followed, but never guaranteed. A permission is *enforced* by the app, and the model can't get past it. A tool is *exact*, but only when it's used, and whether the agent uses it is itself a soft rule. That's what the receipt is for: it shows whether the tool ran. When a rule really matters, ask which kind it is.

**If your change doesn't seem to work:** start a new session. Check that you edited the copy in *your* folder, not the one in the course folder.

**Try it yourself.** Write a whole new skill that uses the tools you have: *crit order* (everyone, in a fair order), *area check* (add up rooms, compare with a target), *random client* (roll to build one from lists), or a *board game referee*. Ask Claude for a new folder in `.claude/skills/`, starting from `add-up` or `tie-breaker`, and rewrite the text until it says what you mean. Then swap with your partner: can you find a request that makes their skill break its own rules?
