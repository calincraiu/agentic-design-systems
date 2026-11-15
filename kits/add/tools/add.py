# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""A tool: adds numbers and prints the total. This is the whole thing."""
import argparse
from decimal import Decimal, InvalidOperation

parser = argparse.ArgumentParser(description="Add numbers and print the total.")
parser.add_argument("numbers", nargs="+", help="The numbers to add, separated by spaces, for example 12.4 18.75 9.3")
args = parser.parse_args()

try:
    numbers = [Decimal(n) for n in args.numbers]
except InvalidOperation:
    parser.error("every input must be a plain number, like 12.4 or -3 (no commas, no units)")

total = sum(numbers)
print("Numbers:", *numbers)
print("Total:", total)
