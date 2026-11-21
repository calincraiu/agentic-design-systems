<!-- layout: statement | where: app -->
<p class="kicker">Before the long runs</p>

# A conversation has a size limit

<p class="lead">New task, new session. What must last goes in <code>CLAUDE.md</code> or a skill.</p>

<!-- notes -->
Every time you send a message, the app sends the model the **whole conversation** so far: your messages, Claude's replies, and the output of every tool it ran. The model can only take in a fixed amount of text at once, measured in tokens (Session 1). That amount is the **context window**.

Today's runs are long. One design request can run a tower and three measures for each of three variants, and every one of those outputs goes into the conversation. When the conversation nears the limit, the app **compacts** it: it replaces older parts with a summary. Details from early on, such as an answer you gave or a number from the first variant, can come out blurred or lost.

Starting a new session clears the conversation. Your files stay as they are, and Claude reads `CLAUDE.md` and the skills fresh at the start of every session. That's why the task slides today say "new session": anything that has to survive from one task to the next belongs in a file, not in the chat.
