<p class="kicker">Part 1 · The smallest possible system</p>

# An agent decides what to do next

Watch the demo in Claude's **Code** tab:

> Roll two dice until you get a double. Tell me how many tries it took.

Nobody said how many times to run the tool, or when to stop. Claude worked that out, reading each result as it went.

An **agent** is an LLM that can use tools and decide what to do next: read files, run tools, look at results and try again, within limits you set.

<div class="box" markdown="1">
**LLM** writes text · **tool** does one exact thing · **agent** = LLM + tools + deciding what's next
</div>
