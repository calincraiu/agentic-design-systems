<!-- layout: task | where: code-yours | time: 35 min | pairs -->
<p class="kicker">Part 3 · A skill that judges · your turn</p>

# Write the judge: tower-check

1. **Open** `.claude/skills/tower-check/SKILL.md` in your folder.
2. **Write** *What I care about*: two or three sentences, in your words.
3. **Fill** the Measures table: `park_sun`, your `daylit`, and one more if you like. Paste each row from its contract, **set your own limit**, and write why.
4. **New session:** *"Check my tower with tower-check."*

<details><summary>The skeleton you start from</summary>
<div data-widget="file" data-path="kits/site/.claude/skills/tower-check/SKILL.md" data-render="markdown" data-title=".claude/skills/tower-check/SKILL.md"></div>
</details>

> **You're done when** the report gives each measure a value, your limit and PASS or FAIL, and every value has a receipt.

<!-- notes -->
#### What you're building
`tower-check`: the skill that judges a tower. It runs the measures you choose and compares each result with your limit. The skeleton came in the `site` kit; you write the part that decides.

#### Steps
1. **Open** `.claude/skills/tower-check/SKILL.md` in your folder.
2. **Write** *What I care about*: two or three sentences on what a good tower on this site must do.
3. **Paste** a row for each measure into the Measures table, replacing *(none yet)*: `park_sun`, your `daylit`, and one more if you like. *Each contract ends with its row, under "Use it in a skill".*
4. **Set** your own limit in each row, and replace *(your reason)* with one sentence on why that number.
5. **Start** a new session and ask *"Check my tower with tower-check."*

#### Background
The skeleton's name, its description (which tells Claude when to use it), and its *How to check*, *Report* and *Rules* sections are already written. *What I care about* and the Measures table are what decide whether a tower passes.

The limit in each pasted row is a starting guess, not a rule. `park_sun` starts at `sun_lost_percent < 20`, from the UK's BRE guide *Site layout planning for daylight and sunlight* (BR 209), which treats an open space that keeps less than 0.8 times its former sunlight, a loss of more than 20%, as noticeably affected. The tool applies that idea to the park's average sun hours. A row with its reason looks like this:

```
| tools/daylit/daylit.gh | floors = the tower run's floors layer, depth = 7 | daylit_percent >= 85 | Most desks within 7 m of a window. |
```

The measures you can choose from:

| Measure | It asks | It can't tell you |
|---|---|---|
| `park_sun` | How much of the park's sun does the tower take? | Any day but 21 March · where people sit |
| `neighbours_sun` | How much sun do the buildings around it lose? | Which neighbour · where the windows are |
| `river_view` | How much of the tower do people on the river see? | Whether they notice it |
| `terraces` | How much open roof do the floors leave? | Whether a terrace is usable |
| `daylit` (yours) | How much of the floor area is near a window? | Where the windows are |

The skill runs measures and reports. It never designs, and it's told never to change your limits: a tower that fails is a finding.
