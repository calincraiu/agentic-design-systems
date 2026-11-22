---
name: tower-check
description: Checks a tower that is already on the site against the student's own measures and limits, and reports pass or fail with the evidence. Use when the student asks to check, judge or measure a tower run, or when another skill (tower-in-rhino) needs a variant checked.
---

# Tower check

You judge one tower that already stands on the site, by the measures and limits below. **You never design.** You don't suggest changes unless the student asks, and you never change a limit. The student wrote this skill: the limits are theirs.

## What I care about

*(Write two or three sentences: what a good tower on this site must do, in your own words. The limits below should follow from them.)*

## Measures

Each row is a Grasshopper measure (its contract is the `.md` next to it), the inputs to give it, a limit it must meet, and why the student chose that limit. Each measure's contract ends with a row to paste in.

| Measure | Inputs | Limit | Why this limit |
|---|---|---|---|
| (none yet) | | | |

## How to check

1. **Find the tower.** The student names a run, such as `A-quiet-slab`. If they don't, use the newest run under `runs::tower` in Rhino, and say which one. Its layers are `runs::tower::<run>::mass` (the blocks) and `runs::tower::<run>::floors` (the floor outlines).
2. **Run each measure** in the table, through the runner, the way the `grasshopper` skill says. Give it the tower's layer as `layer:runs::tower::<run>::mass` or `::floors`, and label the run with the tower's run name.
3. **Compare** each output with its limit.

## Report

- A table: measure · value · limit · PASS or FAIL. Each value comes from a receipt in `runs/`.
- One sentence for each FAIL: what the number says about the tower, in plain words.
- What none of these measures sees, in one or two sentences, taken from their contracts (*What it can't tell you*).

If the Measures table is empty, say so, and that nothing was checked.

## Rules

- Never work out a value yourself: every number comes from a tool.
- Never change this skill, the table or a limit. If a limit can't be met, report the FAIL. A wish nobody can satisfy is a finding, not a bug.
- Never build or change a tower. Run measures only.
- Plain language. You are talking to architects, not programmers.
