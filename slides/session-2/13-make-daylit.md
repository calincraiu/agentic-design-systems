<!-- layout: task | where: rhino | time: 40 min | pairs -->
<p class="kicker">Part 2 · A chain on the site · your turn</p>

# Make a measure: how much of the tower is daylit?

1. **Contract first.** Copy the template to `tools/daylit/daylit.md`. Fill it in, with three test cases **by hand**.
2. **Build** it in Grasshopper (recipe in the notes).
3. **Name** the inputs `in:floors`, `in:depth` and the outputs `out:daylit_percent`, `out:dark_m2`.
4. **Save** it as `tools/daylit/daylit.gh`.
5. **New session:** *"Run my daylit tool on the test cases in its contract."* Then run it on your tower.

> **You're done when** your test cases pass, including a tower so slim that nothing is dark.

<!-- notes -->
#### What you're building
`daylit`: a measure that reads a tower's floor outlines and says how much of its floor area is within `depth` metres of the façade (7 m by default). Inputs `in:floors`, `in:depth`; outputs `out:daylit_percent`, `out:dark_m2`.

#### Steps
1. **Write the contract** first: copy the template to `tools/daylit/daylit.md`. The rule: offset each floor outline inward by `depth`; what's left inside is the dark core; daylit share = 100 × (1 − dark area ÷ floor area).
2. **Work out three test cases** on paper. *A 20 × 20 m tower with `depth = 7` has a 6 × 6 m core on each floor. A 12 × 12 m tower has none: 7 m from each side reaches past the middle.*
3. **Build** it in Grasshopper. Double-click the canvas and type a name to place each one:
    1. A **Curve** parameter (under Params), `in:floors`, and a **Number Slider** `in:depth`: 3 to 12, one decimal, 7.
    2. **Negative**, from `in:depth`. *Inward is a negative distance for the tower's outlines.*
    3. **Offset Curve**: Curve from `in:floors`, Distance from Negative. Then **Area**, from the offset curves.
    4. **Merge**: Area's result into the first input, a **Number** parameter set to 0 (right-click › Set Number) into the second. *So a slim tower gives 0, not nothing.*
    5. **Mass Addition**, from Merge; right-click its input › **Flatten**. *Offset Curve gives one list per floor.* This is the dark area.
    6. A second **Area**, from `in:floors`, into a second **Mass Addition**: the whole floor area.
    7. **Expression**, set to `100*(1-y/x)` (right-click it). Floor area into `x`, dark area into `y`.
    8. Two **Panels**: `out:daylit_percent` and `out:dark_m2`.
4. **Save** it as `tools/daylit/daylit.gh`.
5. **Start** a new session and ask Claude to run your test cases. *It builds each test tower with the tower tool, then gives yours the run's `floors` layer.*
    - "Curve offset failed" on a slim tower is expected: no floor has a core.
    - A test case fails: ask who was wrong, the definition or the contract, and fix that one.
6. **Run** it on your tower from the last task.

#### Background
Daylight from a side window only reaches so far into a room. A common rule of thumb puts useful daylight within about 2 to 2.5 times the height of the window head; Christoph Reinhart tested how far that rule holds in a 2005 simulation study (*A simulation-based review of the ubiquitous window-head-height to daylit zone depth rule-of-thumb*, Building Simulation conference). With windows reaching 2.8 m above the floor, that's about 7 m. A deep floor plate gives more floor area, but its middle needs electric light all day.

The tool treats the whole outline as glass with open sky beyond. Where the windows actually are, the neighbours' shadow, and whether the core is where the lifts and stairs go anyway are things it can't tell you: say so in the contract.

Without the 0 in step 3.4, a tower with no dark core gives empty outputs instead of 0. The slim-tower test case is the one that catches it.

If you have a Grasshopper definition from studio that reads floor outlines or a mass, you can make that your tool instead: the same names, the same contract.
