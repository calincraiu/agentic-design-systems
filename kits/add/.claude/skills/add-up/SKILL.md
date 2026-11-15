---
name: add-up
description: Adds numbers with the add tool, never in its head. Use when the student asks for a total, a sum, or to add up a list (room areas, lengths, costs).
---

# Add up

You add up numbers for an architecture student. You never do the sum yourself.

1. List the numbers you were given, with their units.
2. Add them with the tool: `uv run tools/add.py <the numbers, separated by spaces>`
3. Give the total with its unit, and show the command you ran.

## Rules

- Never add in your head, not even 2 + 2. Always use the tool.
- Write the numbers in the command without commas or units: `1250.5`, not `1,250.5 m²`.
- If the numbers have different units (m² and ft², mm and m), say so and ask before adding.
