---
name: prove-task
description: Software factory stage 05. Proves each acceptance criterion and invariant of a task with tests that would fail if the behavior broke, plus a real browser check for UI changes.
---
# prove-task - evidence, not reassurance

## Steps
1. List every `AC-n` and `INV-n` in the issue. For each, pick the proof: the lowest-level automated test that still exercises what a user or caller observes; a real browser check for UI flows; command output for config or operations.
2. Write tests in the repo's existing framework and style, next to similar tests. Put the criterion ID in the test name.
3. Make sure each core test can fail: break the implementation on purpose, watch the test go red, then restore it.
4. Assert what a user or caller sees, not internals. Mock only outside boundaries (network, clock, third-party APIs), never the unit under test.
5. Run the new tests, then the profile's full test and lint/typecheck commands.
6. For UI changes: start the profile's dev server, walk each flow in a real browser, and note what you saw. Check that every new control works with the keyboard. If the profile has a preview url command, walk the same flows on the PR's preview deploy once CI has built it.
7. Write the proof table for the PR body and `build.md`:

| Criterion | Evidence |
|---|---|
| AC-1 | `test name`: pass |
| INV-2 | `command`: what the output showed |

A criterion with no evidence is unproven. Say so; do not paper over it.
