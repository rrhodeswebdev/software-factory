# 02_spec - what done looks like, testably

One job: turn the issue into a spec a builder can finish without making a product decision.

Agent: `factory-spec`. Paths are from the factory root.

## Inputs
- Working (this task): `tasks/{id}/issue.md`, `tasks/{id}/history.md`, `tasks/{id}/01_triage/triage.md`
- Working (this task): the repo's worktree. Read it; change nothing.
- Working (on a retry): the builder's reason in `history.md` (a `fail: retry 02` from 03 names the gap)
- Reference (every task): `_shared/rules.md`, `_shared/history.md`
- Reference (every task): `repos/{dir}.md`

Do NOT load: other tasks, files the triage didn't point to unless the spec needs them.

## Process
1. Read `history.md` and `triage.md`. Apply any person's feedback; on a retry, close the gap the builder named and change nothing else.
2. Read the code the task touches: the entry points, the helpers it should reuse, the existing tests next to it.
3. Write `spec.md`:
   - **Goal**: one sentence.
   - **Acceptance criteria**: `AC-1`, `AC-2`, ...: each an observable result, with how it will be proved (unit test, integration test, command output, browser check). Three to eight.
   - **Invariants**: `INV-1`, ...: what must not change (existing behavior, APIs, data). Skip if none.
   - **Approach**: files likely touched, existing code to reuse, the smallest design that works. No alternatives essay.
   - **Out of scope**: what the builder must not do.
   - **UI**: `yes` if a person will see the change in a browser or app, else `no`.
   - **Decisions**: every choice you made that the issue left open, and why. A choice that is really the author's (product direction, money, data loss, breaking an API) is not yours: stop with `fail: human`.
4. Self-check before the verdict: each AC is testable and would fail if the feature broke; nothing in Approach contradicts an INV; nothing needs guessing.

## Outputs
- `tasks/{id}/02_spec/spec.md`
- `tasks/{id}/02_spec/check.md`: `pass`, or `fail: human - <the decision needed, with your recommended answer>`
- A handoff appended to `tasks/{id}/history.md`.

## Check
The self-check in step 4, then the builder: 03 sends the spec back with `fail: retry 02 - <gap>` when it can't build without guessing. The review panel and the approver test every AC again.
