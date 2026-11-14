# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""A tool: rolls dice and prints the result. This is the whole thing."""
import argparse
import random

parser = argparse.ArgumentParser(description="Roll dice and print the result.")
parser.add_argument("--sides", type=int, default=6, help="Sides on each die, at least 2 (default 6).")
parser.add_argument("--count", type=int, default=1, help="How many dice to roll, at least 1 (default 1).")
args = parser.parse_args()

if args.sides < 2 or args.count < 1:
    parser.error("a die needs at least 2 sides, and you must roll at least 1")

rolls = [random.randint(1, args.sides) for _ in range(args.count)]
print("Rolls:", *rolls)
print("Total:", sum(rolls))
