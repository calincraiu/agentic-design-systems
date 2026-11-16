<!-- layout: split | where: app -->
<p class="kicker">Groundwork</p>

# Everything you'll write is a text file

<div class="cols" markdown="1">
<div markdown="1">

```
ads-yourname/                  your folder
├── CLAUDE.md                  notes Claude reads first
├── .claude/skills/…/SKILL.md  know-how, as text
├── tools/add.py               a tool
└── runs/                      what the tools made
```

> A text file is only words. You can open it in any editor, and so can Claude.

</div>
<div markdown="1">

```markdown
# Project notes
Keep answers short and in plain language.
Say which file you changed.

## Rules
- Never make up a number: use the tools.
```

<p class="muted">CLAUDE.md: standing instructions, an example only</p>

</div>
</div>

<!-- notes -->
**The idea.** Everything you author in this course is a **plain text file**: words, with no hidden formatting, unlike a Word document. A few terms:

- A **folder** holds files and other folders, like a project folder with drawings, specs and correspondence.
- The **extension** at the end of a file's name says what kind of file it is. `.md` is **Markdown**, notes written by people: `#` starts a heading, `-` starts a list item, `**bold**` is bold. `.py` is **Python**, a small program, which in this course means a tool.
- A name starting with a dot, like `.claude`, makes a **hidden folder**. Your file browser doesn't show it unless you ask. On a Mac, press Cmd + Shift + . in Finder. On Windows, choose View › Show › Hidden items in File Explorer.

The `CLAUDE.md` on the slide is only an example of the *shape*: a heading, a few standing instructions, a rule. What goes in yours is up to you, and you'll write it later today.

**Why it matters.** Because it's all text, you can read every part of the system, change it, and see what changed. Nothing is locked inside an app. Your design approach becomes a document you can share, compare and improve, like a practice's design guide.

**Try it yourself.** In the course folder, open `kits/add/.claude/skills/add-up/SKILL.md` in a plain text editor (Notepad, TextEdit, VS Code). Later today you'll watch this file change what Claude does. It's under twenty lines of plain English: you could have written it.
