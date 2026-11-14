# <Tool name>: what it does, in one sentence

<!-- Copy this file to tools/<your_tool_name>.md and fill in every section.
     You are writing the contract. Claude writes the code to match it, not the other way round. -->

## Who asks, and why
Who would use this, and what question does it answer? One or two sentences.

## Inputs
Everything the tool can be told. Nothing else can change its answer.

| Name | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `--example` | m | 1 to 10 | 3 | What this number is |

## What it does
The rule, step by step, in words. Someone with a calculator should be able to follow it.

1. ...
2. ...

## Output
Exactly what it prints, line by line. Include the units.

## It refuses when
Inputs it must reject with an error instead of an answer.

## Test cases
Worked out **by hand**, before the tool exists. They are how you'll know the tool is right.

| Inputs | Expected output |
|---|---|
| `--example 3` | ... |

## What it can't tell you
What a person might expect it to know, but it doesn't.
