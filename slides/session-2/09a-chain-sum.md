<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · A Grasshopper tool</p>

# Three numbers, a tool for two

<div data-widget="figure" data-name="chain-sum" data-start="1"></div>

<!-- notes -->
`sum` adds two numbers, but you can ask Claude to add three. Claude works out that it can run the tool twice: first on the first two numbers, then on that result and the third. It reads the first result from the runner's output, puts it into the second run, and reports the final answer. Each run follows the contract and leaves its own receipt in `runs/`.

This is the same idea as the chain you build later in the session, where one tool's output is the next tool's input, except that here Claude does the planning and no one built the chain. It works, and it has costs. A list of ten numbers takes nine runs, each with a permission prompt. Each intermediate result also has to pass through the tool's limits: a running total above 1000 is refused, because `in:a` stops at 1000.

Ask Claude to add 12.5, 30 and 7.5 with `sum`, then open the two receipts in `runs/` and find the first result in the second one.
