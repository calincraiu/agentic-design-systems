# Concepts: the parts of an agentic design system

These words get used loosely. In this course they mean specific things, and each one has a concrete example in the course kits, which you copy into your own folder.

## The parts

**LLM.** A large language model: the AI itself. It continues text with what is likely to come next. That's how it knows 2 + 2, and why it can't reliably add two long numbers, roll a fair die or measure a floor plate: it can only write something that fits.
> Here: what you get in the Chat tab.

**Tool.** A capability with defined inputs and outputs that an agent can use. A tool really does what it says, and it doesn't get creative about it.
> Here: `tools/add.py` takes numbers and returns their exact total. `tools/dice.py` takes a number of sides and a count, and returns rolls. `tools/tower/tower.py` takes eight numbers and returns geometry, metrics and an image. `tools/stair_check.py` was built from a contract someone wrote in plain language. Claude also has built-in tools, for reading files, writing files and running commands.

**Agent.** An LLM that can use tools and decide what to do next: read files, run tools, look at results and try again, within limits you set.
> Here: Claude, in the Code tab. Rolling until a double, it decides by itself when to stop.

**Skill.** Reusable know-how: instructions (and any supporting files) that tell the agent *how to approach* a kind of task. A skill doesn't *do* anything by itself; it shapes how the agent uses its tools.
> Here: `.claude/skills/add-up/SKILL.md` (never add in your head) and `.claude/skills/tie-breaker/SKILL.md` (roll exactly once). They are plain text, and you can write one.

**Workflow.** The sequence of steps, decisions and checkpoints that connects everything. It can live inside a skill, in code or in your head.
> Here: the steps in the tower-designer skill: you describe → the agent asks → *you answer* → the tool builds and checks three → report, and you choose.

**Context.** Everything the agent knows when it starts working: the conversation, the files it reads and the project instructions.
> Here: the `CLAUDE.md` in your folder, loaded at the start of every session, and your brief.

**Metric.** A number the tool measures, so that "better" can be argued rather than asserted. The list of metrics decides what the system is able to notice.
> Here: the `METRICS` list in `tools/tower/tower.py`. Look for what's missing from it.

## Who does what

| Job | Best done by | Why |
|---|---|---|
| Reading a vague, emotional brief | the **agent** | good with ambiguity and language |
| Making exact geometry | a **tool** | the same input always gives the same output |
| Measuring and checking limits | a **tool** | numbers must be right, not plausible |
| Proposing and comparing options | the **agent**, using the tools | it can explore quickly and explain trade-offs |
| Deciding what is good | **you** | that is design |

An image or a confident paragraph is not evidence. The metrics are, as far as they go.

## The loop

```
 you describe ──► the agent asks ──► you answer ──► brief
                                                      │
          ┌───────────────────────────────────────────┘
          ▼
      GENERATE (tool) ──► MEASURE (tool) ──► COMPARE (agent) ──► DECIDE (you)
          ▲                                                         │
          └───────────── change the brief, the skill, the tool ◄────┘
```

## The ladder of authorship

Over the four sessions you move from *using* an agent to *designing the system it works in*:

1. **Prompt**: asking for things
2. **Context**: writing the brief and project instructions ← *Session 1*
3. **Skill**: encoding your approach ← *Session 1*
4. **Tool**: deciding what a tool takes and returns ← *Session 1 (a first contract), Session 2*
5. **Measure**: deciding what "good" means, in numbers ← *Session 2*
6. **Workflow**: connecting it all, with your decisions built in ← *Sessions 3–4*

## Checkpoint questions

- What is the difference between a tool and a skill? Give an example of each from your folder.
- You know 2 + 2 without calculating. Why is that a good picture of how an LLM answers, and why does it go wrong for long numbers?
- Why can't an LLM on its own pick fairly? What happened when the room asked it for a crit order?
- Why does the tower designer stop and ask questions before generating anything?
- Claude says a variant is "elegant and grounded". What would you check before believing it?
- Why does each limit in the brief record where it came from?
- If you want "lots of terraces", which part of the system would have to change to measure that?
- What happens to the design if you change the skill, and what happens if you change the tool?
