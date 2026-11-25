<!-- layout: diagram | where: app -->
<p class="kicker">Part 1 · A Grasshopper tool</p>

# Named inputs, named outputs, a contract beside it

<div data-widget="figure" data-name="gh-tool" data-start="0" data-ghost></div>

<!-- notes -->
Any Grasshopper definition can become a tool. It needs three things:

- **Inputs** with nicknames starting `in:`. A Number Slider is the usual one, because its minimum, maximum and decimal places say exactly what the tool accepts. A Value List (a dropdown) works the same way with names, and a Curve or Geometry parameter takes objects from a Rhino layer, such as `layer:Site::Park`.
- **Outputs** with nicknames starting `out:`. A Panel shows its value on the canvas, which makes it easy to check by eye. Numbers and text are reported; geometry is baked into Rhino.
- **A contract**, `<name>.md`, in the same folder as `<name>.gh`. It says in plain words what each input means and its unit, the rule, what comes out, and test cases worked out by hand.

The **nickname** is the short name a Grasshopper object shows on the canvas. To change it, right-click the object and edit the name at the top of the menu. Everything without `in:` or `out:` is inside the tool, and Claude never touches it.

The folder layout matters: a tool lives in `tools/<name>/` as `<name>.gh` and `<name>.md`, with the same name. That way Claude and you find the contract for any tool without searching.
