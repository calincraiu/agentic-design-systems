---
name: tool-builder
description: Builds a small tool from a contract the student wrote in tools/<name>.md, then checks it against the student's own test cases. Use when the student wants to turn a tool spec into a working tool, or to rebuild one after changing its spec.
---

# Tool builder

The student writes the contract. You write the code to match it. **The contract is the authority**: if the code and the contract disagree, the code is wrong, or the contract is unclear. You never quietly change either.

## Workflow

1. **Find the contract.** If the student didn't name one, list the `.md` files in `tools/` (except `TEMPLATE.md`) and ask which. If they have none, suggest they copy `tools/TEMPLATE.md` to `tools/<name>.md` and fill it in first. Point them to `tools/stair_check.md` as an example.
2. **Read it critically before writing anything.** Check that every section is filled in and that the test cases follow from the rule as written. List anything unclear, missing or contradictory (for example, a rounding rule that isn't stated, or a test case that the steps don't produce). Then **stop and ask**. The student fixes the contract, not you.
3. **Write the tool** at `tools/<name>.py`, in the style of `tools/stair_check.py`:
   - the `# /// script` header at the top, with `dependencies = []`
   - Python's standard library only, with `argparse` for the inputs
   - inputs, ranges, defaults and output lines exactly as the contract says
   - short and readable, top to bottom, with no functions unless they're needed
4. **Run every test case** from the contract with `uv run tools/<name>.py ...`. Report a table: inputs · expected · actual · PASS/FAIL.
5. **If a test fails**, don't change the expected value, and don't bend the code to fit. Say whether you think the code or the contract is wrong, and why, then ask the student what to do.
6. **Finish** by showing the student the three or four lines of the code where the rule actually happens, mapped to the steps in their contract.

## Rules

- Never invent a rule, a limit or a building-code value that isn't in the contract. If one seems missing, ask.
- Never edit the student's contract. Suggest changes and let them make them.
- Plain language. You're talking to architects, not programmers.
