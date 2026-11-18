<!-- layout: split | where: app -->
<p class="kicker">Groundwork</p>

# Everything you'll write is a text file

<div class="cols" markdown="1">
<div markdown="1">

```
ads-tutorial/                  your folder
├── CLAUDE.md                  notes Claude reads first
├── .claude/skills/…/SKILL.md  know-how, as text
├── tools/add.py               a tool
└── runs/                      what the tools made
```

> A text file is only words. **`.md` (Markdown)** adds a few marks: `#` for a heading, `-` for a list.

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
Everything you write in this course is a **plain text file**: characters only, with no hidden formatting, unlike a Word document. A few terms used from here on:

- A **folder** holds files and other folders.
- A **path** gives a file's location one folder at a time. `tools/add.py` is the file `add.py` inside the folder `tools`.
- `.md` is **Markdown**, plain text with a few marks for structure. `#` starts a heading, `-` a list item, and `**bold**` makes bold. It reads fine as it is, and some apps display it formatted.
- `.py` is a **Python** program. In this course, that means a tool.
- A name starting with a dot, like `.claude`, is a **hidden folder**. You need hidden items switched on to see it.

The `CLAUDE.md` on the slide only shows the shape of one: a heading, a couple of standing instructions and a rule. You write your own in a few minutes.

Because every part of the system is text, you can open it, read it, change it and compare versions. A design approach written down this way can be shared and revised, much like a practice's design guide.

Open `kits/add/.claude/skills/add-up/SKILL.md` from the course folder in a text editor (Notepad, TextEdit or VS Code). It's eighteen lines of ordinary English, and later today you'll see it change what Claude does.
