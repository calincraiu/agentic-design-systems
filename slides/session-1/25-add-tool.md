<!-- layout: split | where: app -->
<p class="kicker">Part 1 · The tool</p>

# A tool really does the thing

<div class="cols" markdown="1">
<div markdown="1">

<div data-widget="add" data-numbers="2 2"></div>

A **tool** has written-down inputs and outputs. It doesn't guess. Try `1,5 2`: it refuses rather than guess what you meant.

`add.py` is a **program** written in **Python**: the `.py` says so.

</div>
<div data-widget="file" data-path="kits/add/tools/add.py" data-highlight="18" data-title="tools/add.py: the whole tool"></div>
</div>

<!-- notes -->
This is the whole add tool. Reading from the top:

- Lines 1–4 are a header listing what the tool needs to run. This one needs nothing beyond Python itself.
- The line `parser.add_argument("numbers", ...)` defines the **input**, the numbers you give it.
- The highlighted line 18, `total = sum(numbers)`, does the adding.
- The two `print` lines are the **output**.

It uses `Decimal`, which does arithmetic the way you would on paper. Ordinary computer arithmetic gives 0.1 + 0.2 = 0.30000000000000004.

The point of reading it is to see that nothing is hidden. A tool states its inputs and outputs, and for the same inputs it gives the same output every time. That is what makes it suitable for anything you need to measure.

Type `0.1 0.2` into the widget and you get exactly 0.3. Then try `1,5 2`. In much of Europe `1,5` means one and a half, while in the UK and US the comma separates thousands, so it could mean 15. The tool refuses and says why, because it only accepts plain numbers. Ask Chat "what is 1,5 + 2?" and it may ask which you meant, or it may pick one and answer 3.5 or 17. Nothing makes it stop. A tool can be written to refuse unclear input, and deciding what it should refuse is part of designing it.
