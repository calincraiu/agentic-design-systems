# <Tool name>: what it does, in one sentence

<!-- Copy this file to tools/<your_tool>/<your_tool>.md, next to <your_tool>.gh, and fill in every section.
     You are writing the contract. The definition must match it, not the other way round. -->

## Who asks, and why
Who would use this, and what question does it answer? One or two sentences.

## Inputs
Everything the tool can be told. On the canvas, each one is a slider (or a parameter) whose nickname starts with `in:`.
The slider's minimum and maximum are the allowed range: the runner refuses anything outside it.

| On the canvas | Unit | Allowed range | Default | Meaning |
|---|---|---|---|---|
| `in:example` | m | 1 to 10 | 3 | What this number is |

## What it does
The rule, step by step, in words. Someone with a calculator should be able to follow it.

1. ...

## Outputs
Each one is a parameter or a Panel whose nickname starts with `out:`.

| On the canvas | Unit | Meaning |
|---|---|---|
| `out:example` | m² | What this number is |

## Test cases
Worked out **by hand**, before you trust the tool.

| Inputs | Expected output |
|---|---|
| `example = 3` | ... |

## What it can't tell you
What a person might expect it to know, but it doesn't.
