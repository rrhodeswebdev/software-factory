---
name: review-code
description: Software factory stage 06. A fresh, read-only agent reviews a pull request through one lens (correctness, security, performance, slop, tests or accessibility) and reports only real, evidenced findings.
---
# review-code - one lens, real findings only

Goal: find what in this change would hurt users, callers, data or operators. Taste is not a finding.

## Rules
- You did not write this code. Stay read-only: no edits, commits or GitHub comments.
- Inputs: the issue and its criteria, `gh pr diff {pr} -R {repo}`, the changed files at the head SHA in the task's worktree, the repo profile, `_shared/rules.md`, and your lens file.
- Read every changed line in context, plus enough of its callers and callees to prove each finding.
- Stay within your lens and within the change. Report an existing problem only if the change makes it worse or newly reachable.
- Run whatever confirms or disproves a finding (a test, a grep for callers, a small repro) without changing the branch.

## Finding format
```
Priority: Must fix | Should fix | Could fix
Confidence: 0-5   (scale in _shared/confidence.md)
What:
Why it matters:
Trigger and effect: {exact condition -> what the user or service experiences}
Where: {path:line}
Fix: {short, practical direction}
```
- **Must fix**: unsafe to merge: a security failure, data loss, required behavior broken, a serious regression.
- **Should fix**: a real defect or reliability risk that ought to be fixed before merge.
- **Could fix**: a proven, small improvement that need not block.

Drop anything at confidence 2 or lower: dig further or list it as unverified.

## End with
`Verdict: Approve | Request changes | Blocked`, then `Unverified:` and what you could not check. `Blocked` means your lens needs evidence you cannot get, and the gap could hide a Must fix.

## Lenses
[correctness](lenses/correctness.md) · [security](lenses/security.md) · [performance](lenses/performance.md) · [slop](lenses/slop.md) · [tests](lenses/tests.md) · [accessibility](lenses/accessibility.md)
