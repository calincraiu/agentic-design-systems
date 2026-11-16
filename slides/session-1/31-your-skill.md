<!-- layout: task | where: code-yours | time: 25 min | pairs -->
<p class="kicker">Your turn</p>

# Write your own skill, with the tools you have

1. Decide what the skill does, and what it must **never** do.
2. Ask Claude for a new skill in `.claude/skills/`, starting from `add-up` or `tie-breaker`.
3. **Rewrite the text** until it says what *you* mean. This part is yours.
4. Start a **new session**, run it, and adjust.

- *Crit order*: everyone, in a fair order
- *Area check*: add up rooms, compare with a target
- *Random client*: roll to build one from lists
- *Board game referee*

> **You're done when** your skill works and you can answer: **what can your skill not make the tool do?** Try asking it for a 7 on a six-sided die.

<!-- notes -->
**The idea.** You write a skill that uses the tools you already have. Let Claude create the file, but the words are your job. Read every line and change anything that doesn't say what you mean. That's the authorship.

**The question at the end** is the important one. Ask your skill for a 7 on a six-sided die. The tool *can't* roll a 7. But the LLM can still *write* "I rolled a 7", because writing is all it needs to do that. A skill can tell it not to, and the rule in your `CLAUDE.md` helps. Only the tool guarantees what actually happened, though. That's why the output of the tool, not the agent's description of it, is the evidence.

**If your skill doesn't show up:** start a new session. If it's still missing, check that the file is called exactly `SKILL.md` and sits directly in `.claude/skills/<name>/`.

**Try it yourself.** Swap skills with your partner. Can you find a request that makes their skill break its own rules?
