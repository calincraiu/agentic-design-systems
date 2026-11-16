<!-- layout: split | where: app -->
<p class="kicker">Part 1 · The tool</p>

# A tool really does the thing

<div class="cols" markdown="1">
<div markdown="1">

<div data-widget="add" data-numbers="2 2"></div>

A **tool** has written-down inputs and outputs. It doesn't guess. Try `1,5 2`: it refuses rather than guess what you meant.

</div>
<div data-widget="file" data-path="kits/add/tools/add.py" data-highlight="18" data-title="tools/add.py: the whole tool"></div>
</div>

<!-- notes -->
**The idea.** This is a complete tool, and it fits on a postcard. Read it from the top:

- Lines 1–4 list what the tool needs in order to run. This one needs nothing extra.
- `parser.add_argument("numbers", ...)` is the **input**: the numbers you hand it.
- The highlighted line, `total = sum(numbers)`, is where the adding actually happens.
- The two `print` lines are the **output**: what comes back.

It uses `Decimal`, which counts the way you would on paper. Plain computer arithmetic would say 0.1 + 0.2 = 0.30000000000000004.

**Why it matters.** You don't need to write tools like this, but it helps to see there's no magic in them. A tool is a promise in writing: give me *these* inputs and you get *this* output, the same way every time. That promise is what makes it trustworthy for measuring.

**Try it yourself.** Type `0.1 0.2` into the widget: exactly 0.3. Then type `1,5 2`. In much of Europe `1,5` means one and a half; in the UK and US a comma separates thousands. The tool refuses, and tells you why. Now ask Chat "what is 1,5 + 2?". It will answer anyway, with 3.5 or 17, because an LLM always produces *something*. **A tool can say "I can't". An LLM guesses.** Refusing is a design decision too.
