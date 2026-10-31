"""Tower Toy: a stacked-floor tower that can twist, taper and lean.

The worked example for Session 1. Its parts:
  params.py    the parameters (the tool's contract)
  generate.py  the Python generator (the same tower as tower.gh, without Rhino)
  evaluate.py  the metrics and constraint checks
  cli.py       the commands the agent calls: `uv run tower ...`
  tower.gh     the Grasshopper generator, driven through the bridge
"""
SYSTEM = "tower"
