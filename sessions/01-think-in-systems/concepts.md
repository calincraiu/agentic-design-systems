# Concepts: the parts of an agentic design system

These words get used loosely. In this course they mean specific things, and each one has a concrete example in this repo.

## The parts

**Agent.** An AI model that can decide what to do next: read files, run tools, look at results, and try again, within limits you set.
> Here: Claude Code, in VS Code. It reads the client card, writes the brief, calls the tower tools and compares the results.

**Tool.** A capability with defined inputs and outputs that the agent can use. A tool does exactly what it says, the same way every time.
> Here: `uv run tower generate --floors 20 --twist 90`. It takes eight numbers and returns geometry, metrics and an image. Run `uv run tower params` to read its contract. Claude Code also has built-in tools: reading files, writing files, running commands.

**Skill.** Reusable know-how: instructions (and supporting files) that tell the agent *how to approach* a kind of task. A skill doesn't *do* anything by itself; it shapes how the agent uses its tools.
> Here: [.claude/skills/tower-designer/SKILL.md](../../.claude/skills/tower-designer/SKILL.md). It is plain text, and you can write one.

**Workflow.** The sequence of steps, decisions and checkpoints that connects everything. It can live inside a skill, in code, or in your head.
> Here: steps 1–7 in the tower-designer skill: read → interpret → check → *ask the client* → generate → evaluate → report.

**Context.** Everything the agent knows when it starts working: the conversation, the files it reads, and the project instructions.
> Here: [CLAUDE.md](../../CLAUDE.md), loaded at the start of every session, and the structured brief, which is context written as data.

**MCP (Model Context Protocol).** A standard plug that lets AI applications discover and use tools made by others. It's useful for connecting systems, but not needed to understand them. We'll come back to it.

## Who does what

| Job | Best done by | Why |
|---|---|---|
| Reading a vague, emotional brief | the **agent** (LLM) | good with ambiguity and language |
| Making exact geometry | a **tool** (Grasshopper or Python) | deterministic: the same input always gives the same output |
| Measuring and checking limits | a **tool** (the evaluator) | numbers must be right, not plausible |
| Proposing and comparing options | the **agent**, using the tools | it can explore quickly and explain trade-offs |
| Deciding what is good | **you** | that is design |

An image or a confident paragraph is not evidence. The metrics are.

## The loop

```
 client card ──► INTERPRET ──► structured brief ──► you + client answer questions
                                                         │
          ┌──────────────────────────────────────────────┘
          ▼
      GENERATE (tool) ──► EVALUATE (tool) ──► COMPARE (agent) ──► DECIDE (you)
          ▲                                                          │
          └────────────── change the brief, the skill, the tool ◄────┘
```

## The ladder of authorship

Over the four sessions you move from *using* an agent to *designing the system it works in*:

1. **Prompt**: asking for things
2. **Context**: writing the brief and project instructions ← *Session 1*
3. **Skill**: encoding your design approach ← *Session 1*
4. **Tool contract**: deciding what a tool takes and returns ← *Session 2*
5. **Evaluator**: deciding what "good" means, measurably ← *Session 2*
6. **Workflow**: connecting it all, with your decisions built in ← *Sessions 3–4*
