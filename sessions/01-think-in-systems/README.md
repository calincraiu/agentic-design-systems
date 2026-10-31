# Session 1 · Think in systems

**By the end of this session you will have** run a complete agentic design system, taken it apart, turned a client's words into a structured brief, and written your first skill: a design stance that changes how the agent designs.

## Plan (3 hours)

| Time | What | Where |
|---|---|---|
| 0:00 | **Demo.** A client card goes in; a tower appears in Rhino; three options come out | watch |
| 0:20 | **E1** · Set up and make a first tower | [exercises.md](exercises.md) |
| 0:45 | **Concepts.** Agent, tool, skill, workflow, context | [concepts.md](concepts.md) |
| 0:55 | **E2** · Map the system | [exercises.md](exercises.md) |
| 1:15 | Break | |
| 1:30 | **E3** · Brief as data | [exercises.md](exercises.md), [clients/](clients/) |
| 2:10 | **E4** · Write a design stance | [exercises.md](exercises.md), [templates/](templates/) |
| 2:45 | **Mini-crit** · What could your skill not change? | gallery on screen |

## What you'll make

- `studio/briefs/<card>.json`: a structured brief, edited by you
- `.claude/skills/tower-<stance>/SKILL.md`: your design stance
- runs in `runs/` comparing Balanced and your stance on the same brief

## Useful commands

You can ask the agent to run these, or run them yourself:

```
uv run tower params              # what the tower can do and measure
uv run kit gallery --open        # compare all runs
uv run kit ping                  # is Grasshopper listening?
```
