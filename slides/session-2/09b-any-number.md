<!-- layout: task | where: rhino | time: 15 min | pairs -->
<p class="kicker">Part 1 · A Grasshopper tool · stretch</p>

# Add any amount of numbers

1. **Save** a copy of `sum.gh` as `tools/sumall/sumall.gh`.
2. **Replace** the two sliders with one Number parameter, `in:numbers`.
3. **Replace** Addition with Mass Addition. Wire its *Result* to `out:sum`.
4. **Change** the contract to match, then ask Claude to add five numbers.

> **You're done when** Claude adds five numbers you chose, and `sumall.md` says what the tool now accepts and what it no longer refuses.

<!-- notes -->
#### What you're building
A second version of the adding tool that takes a list of any length in one run, instead of Claude chaining two-number runs. The point is to change a tool's definition and its contract together, and to see what the change costs.

#### Steps
1. **Save** a copy: File › Save As, in a new folder `tools/sumall`, as `sumall.gh`. *The original `sum` stays as it was.*
2. **Delete** the two sliders and the Addition component.
3. **Place** a Number parameter (Params › Input › Number) and **rename** it `in:numbers`. *This is a plain parameter, so it holds a list and has no range.*
4. **Place** a Mass Addition component (Maths › Operators) and wire the parameter into it.
5. **Wire** Mass Addition's **Result** output, not Partial Results, into the Panel named `out:sum`. *Partial Results is the running total after each number, a list.*
    - If the Panel shows a list: you used Partial Results. Move the wire.
6. **Copy** `sum.md` to `tools/sumall/sumall.md` and change it: one input row, `in:numbers`, a list of numbers of any length; the rule now adds them all; new test cases, such as `[12.5, 30, 7.5]` giving `50` and `[5]` giving `5`. Remove the test cases that were refused.
7. **Ask** Claude to run it with five numbers of your choice. Check the answer by hand.
8. **Answer** in the last section of the contract, *What it can't tell you*: what did the tool refuse before that it now accepts?

#### Background
A slider's minimum, maximum and decimal places were the tool's guard: the runner refused anything outside them. A Number parameter has no such limits, so `2000`, `-5` and `0.125` all go through. Nothing in the definition says what counts as a reasonable number, so the contract has to, and nothing but your own reading of the result will catch a wrong value. If you want a limit back, the definition needs components that check the numbers.

Claude gives the runner the whole list in one go, for example `{"numbers": [12.5, 30, 7.5, 1, 4]}`. The receipt in `runs/` records the list. The two outputs of Mass Addition, *Result* and *Partial Results*, are worth a look in a Panel each, to see the difference.

What the tool does with an empty list is not settled by the contract you started from. Try it, and write down what you see.
