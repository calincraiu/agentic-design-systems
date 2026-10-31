# Agentic Design Systems

A course workspace for designing with AI agents. You won't just *use* an AI here. You'll build the system it works inside: the briefs it reads, the skills that shape its judgement, the tools it calls and the measures that say what "good" means.

## Getting started

1. Put this folder somewhere normal on your computer, such as `Documents/ads-course`. Avoid Downloads, and avoid OneDrive or iCloud folders if you can.
2. Open the **Claude desktop app**, go to the **Code** tab and choose this folder. (VS Code with the Claude Code extension works the same way, if you prefer it.)
3. Type **`/setup`**. Claude installs what's needed and checks that everything works. Read what each command does before you approve it.

Then start [Session 1](session-1/1-dice.md).

## What's in here

| Folder | What it is |
|---|---|
| [session-1/](session-1/) | The walkthroughs, concepts and client cards for Session 1 |
| [my-work/](my-work/) | **Your workspace**, including your briefs |
| [tools/](tools/) | The tools Claude can use. Start by reading [dice.py](tools/dice.py) |
| [.claude/skills/](.claude/skills/) | Skills Claude can use, including the ones you write |
| `runs/` | Created as you work: one folder per tower, and `runs/gallery.html` to compare them |
| [CLAUDE.md](CLAUDE.md) | What Claude is told about this project at the start of every session |

## Skills you can call

- `/setup`: get this computer ready, or check it when something breaks
- `/tie-breaker`: settle a decision with a real die roll
- `/tower-designer`: design towers for a client card
- `/course-tutor`: explain a concept or some code, or quiz you
