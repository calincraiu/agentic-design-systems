<!-- layout: task | where: code-yours | time: 25 min -->
<p class="kicker">Part 3 · A skill that judges · your turn</p>

# Design with your judge

1. **Paste** your Session 1 stance into *Design stance* in `.claude/skills/tower-in-rhino/SKILL.md`.
2. **New session:** run `/tower-in-rhino` with the Session 1 wish.
3. **Read** the report: which variants passed your check, and what it judged by eye.

> **You're done when** three towers have stood on the site, each checked by your `tower-check`, and you can say which of your limits changed the variant it recommends.

<!-- notes -->
#### What you're building
Three towers for the Session 1 wish, designed by `tower-in-rhino` with your stance, and each one judged by your `tower-check`.

#### Steps
1. **Find** your Session 1 stance: three sentences in your own `tower-<stance>` skill, or in `tower-designer` if you edited it in place.
2. **Paste** them over the *Balanced* paragraph under *Design stance* in `.claude/skills/tower-in-rhino/SKILL.md`.
3. **Start** a new session and run `/tower-in-rhino` with the Session 1 wish. Answer its three questions.
4. **Read** the report: which variants passed, which of your limits decided, and what it judged by eye.

#### Background
`tower-in-rhino` works like `tower-designer` from Session 1: it listens, asks three questions, writes a brief and builds three variants. The differences are that the towers stand on the site in Rhino, Claude looks at each one with a viewport picture, and every variant goes through your `tower-check`. A variant that fails one of your limits gets one revision at most; after that the failure is reported.

Two skills now shape the result, and they do different jobs: the stance says how to design, `tower-check` says what passes.

Sometimes nothing passes. That means your wish and your limits ask for more than this tower tool can give. The design skill isn't allowed to loosen your limits: whether to change a limit, the wish or the tool is your decision.

Whatever your measures don't cover, such as whether the tower is *calm*, the skill can only judge by eye, and the report has to say so.
