# Concepts: the parts of an agentic design system

These words get used loosely. In this course they mean specific things, and each one has a concrete example in the course kits, which you copy into your own folder.

**The six to know.** Session 1 builds one system from six parts: the **LLM**, a **tool**, the **agent**, a **skill**, **context**, and **you**. Learn those first. The other words on this page (workflow, metric, and the rest) are useful, and you'll meet them as the course goes on.

## First: the model and the app

"Claude" names three things: a company's product, a **model** and an **app**. Most of this course depends on telling the last two apart.

**Model.** What training produces: a very large file of numbers that reads text and writes text. It was trained once, on a huge library of text, and then frozen. It has a cutoff date, it doesn't look things up, and it doesn't learn from your conversations. It runs far away, in a data centre.
> Here: Claude's models (Opus, Sonnet, Haiku), which you can choose in the app.

**App.** The program around the model, on your laptop. It shows you the conversation, adds its own instructions, gives the model tools, runs those tools when the model asks, and asks *you* before it acts. Different apps give the same model different equipment.
> Here: the Chat tab and the Code tab are two tabs of one app, each giving the same model different equipment. Everything you author (`CLAUDE.md`, skills, tools, permissions) lives on the app's side.

Whatever the model reads (your messages, files it opens, tool results) is sent to it as text. Check your school's or practice's AI policy before you open project files with any AI app.

## The parts

**LLM.** A large language model: the AI itself. It continues text with what is likely to come next. That's how it knows 2 + 2, and why it can't reliably add two long numbers, roll a fair die or measure a floor plate: it can only write something that fits. In this course, "the LLM" and "the model" mean the same thing.
> Here: the model inside Claude, in both the Chat and the Code tab. On its own, it can only write.

**Tool.** A capability with defined inputs and outputs that an agent can use. A tool really does what it says, and it doesn't get creative about it.
> Here: `tools/add.py` takes numbers and returns their exact total. `tools/dice.py` takes a number of sides and a count, and returns rolls. `tools/tower/tower.py` takes eight numbers and returns geometry, metrics and an image. `tools/stair_check.py` was built from a contract someone wrote in plain language. Claude also has built-in tools, for reading files, writing files and running commands.

**Agent.** An LLM that can use tools and decide what to do next, in a loop the app runs: read files, run tools, look at results and try again, within limits you set. It works in a loop (act, look, decide), so the number of steps isn't fixed in advance, and it stops when *it* judges the job done: you choose the goal and how much it may do unasked.
> Here: Claude, in the Code tab. Rolling until a double, it decides by itself when to stop.

**Skill.** Reusable know-how: instructions (and any supporting files) that tell the agent *how to approach* a kind of task. A skill doesn't *do* anything by itself; it shapes how the agent uses its tools.
> Here: `.claude/skills/add-up/SKILL.md` (never add in your head) and `.claude/skills/tie-breaker/SKILL.md` (roll exactly once). They are plain text, and you can write one.

**Context.** Everything the agent has in front of it while it works: the project instructions, the conversation, the files it reads and what the tools print. Only part of it is there before you ask: your `CLAUDE.md` and your skills' descriptions come back in every new session, and the rest is gone.
> Here: the `CLAUDE.md` in your folder, loaded at the start of every session, and your brief.

**You.** The part that decides what is good. You set the goal, the limits and how much the agent may do unasked, and you choose between the options. That is design.
> Here: every "you choose" in the tower designer's report, and every permission prompt you answer.

## A habit: check the receipt

When an agent tells you what it did, that's more generated text. The **receipt** is the record of what actually ran: the command, and what the tool said back. In the Code tab, expand the tool calls to see it. In the course app, open "Behind the scenes" under any widget. If there's no receipt, nothing ran: it was written, not done.

The receipt can be trusted because the **app** writes it. The model only writes a *request* to run a tool; the app runs it and records what came back.

## A habit: ask which kind of rule it is

- A **soft rule** is text the model *reads*: your `CLAUDE.md`, a skill. Usually followed, never guaranteed.
- A **hard rule** is enforced by the app: a permission. The model can't get past it.
- A **tool** is exact when it's used, but *whether* it's used is a soft rule. The receipt shows whether it ran.

When a rule really matters, make it a hard one, and check the receipt.

## More words

**Brief.** What you want, written down so it can be questioned: your words, how they were read, what was assumed, and the limits, each marked as yours or assumed.
> Here: the file the tower-designer skill writes in `briefs/`.

**Workflow.** The sequence of steps, decisions and checkpoints that connects everything. It can live inside a skill, in code or in your head.
> Here: the steps in the tower-designer skill: you describe → the agent asks → *you answer* → the tool builds and checks three → report, and you choose.

**Metric.** A number the tool measures, so that "better" can be argued rather than asserted. The list of metrics decides what the system is able to notice.
> Here: the `METRICS` list in `tools/tower/tower.py`. Look for what's missing from it.

## Who does what

| Job | Best done by | Why |
|---|---|---|
| Reading a plain-language brief | the **agent** | good with ambiguity and language |
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
4. **Tool**: deciding what a tool takes and returns ← *Session 2*
5. **Measure**: deciding what "good" means, in numbers ← *Session 2*
6. **Workflow**: connecting it all, with your decisions built in ← *Sessions 3–4*

## Checkpoint questions

- What is the difference between a tool and a skill? Give an example of each from your folder.
- Claude says it rolled a 7 on a six-sided die. Which part of the system was responsible, and how would you check?
- You know 2 + 2 without calculating. Why is that a good picture of how an LLM answers, and why does it go wrong for long numbers?
- Why can't an LLM on its own pick fairly? What happened when the room asked it for a crit order?
- Why does the tower designer stop and ask questions before generating anything?
- Claude says a variant is "elegant and grounded". What would you check before believing it?
- Why does each limit in the brief record where it came from?
- If you want "lots of terraces", which part of the system would have to change to measure that?
- What happens to the design if you change the skill, and what happens if you change the tool?
