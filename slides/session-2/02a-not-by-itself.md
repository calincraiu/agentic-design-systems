<!-- layout: diagram | where: app -->
<p class="kicker">Before we start</p>

# Claude can't run a definition by itself

<div data-widget="figure" data-name="gap" data-start="1"></div>

<!-- notes -->
A Grasshopper definition is a file that only Grasshopper can run, and Claude has no hands: it can't open Rhino, move a slider or read a panel. Nothing in Claude or in Grasshopper connects the two. Something has to be built to do it.

Two pieces were built for you, and both come in the `gh` kit you take in Part 1. The **runner** is a short script that opens a definition, sets its inputs, lets it solve and reads its outputs. The **`grasshopper` skill** is a page of instructions that tells Claude when to use the runner and how to ask Rhino to run it. A skill works the same way as the ones from Session 1: it's words, and Claude follows them.

The runner and the skill are why a definition can be run as a tool at all. You don't need to read either. What you need to know is that every tool in this session depends on them, and that this is something a person built, not something Claude or Grasshopper does out of the box.
