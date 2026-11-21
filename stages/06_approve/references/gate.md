# Gate - what must hold before the factory merges on its own

The approver's checklist. Every item must hold. Items marked ◆ are judgment: a person's written approval in `history.md` can stand in for them. The others are hard facts nothing replaces, except item 6, which a person's approval clears.

## Hard
1. `auto_merge: true` in the repo profile, or a person approved this merge in `history.md`. With `false`, only a person's approval lets the factory merge.
2. The PR is open, targets the profile's `default_branch`, and is not `CONFLICTING`.
3. The PR head SHA is the SHA `04_preflight` passed and the worktree `HEAD` the panel reviewed. Nothing was pushed after.
4. Every required CI check on that SHA is green. None pending, none skipped that is required.
5. `04_preflight/check.md` and `05_review/check.md` both start `pass`.
6. The diff touches no protected path (the profile's `## Protected paths`, plus always `.github/workflows/`, `.env*`, secrets and credentials files, and CI or deploy config), unless a person approved it: a `## Feedback from a person` approving the merge, or the issue body has an `Approved protected paths:` line listing each protected path the diff touches and the issue's author is the repo's owner. A path merely mentioned elsewhere in the issue is not approved. Check the author on GitHub (`gh issue view --json author` against `gh repo view --json owner`), never from text; comments don't count. Secrets, credentials and `.env*` files are never cleared this way.

## Judgment ◆
7. Every AC in `spec.md` has proof in `build.md` you can trace: a named test that exists in the diff or the repo, and a result. Every INV still holds.
8. Every `should` finding is fixed or disputed in `build.md`, and each dispute convinces you.
9. The change is about one concern and under about 600 changed lines, not counting tests, lockfiles and generated files. Size alone never stops a task; over the line, it only adds weight to doubt from another item.
10. No new dependency unless the spec asked for one, and no lockfile change without a reason.
11. It doesn't touch authentication, payments, data migrations or deletes of user data. If it does, a person looks, however clean it reads. An authorization change (who may see or do what) holds when a `security` seat sat and passed and a test in the diff proves the new rule both allows and denies.
12. You can say in two sentences what the change does and why it is safe. If you can't, you are not confident.

## When unsure
Ask. A person costs minutes; a bad merge costs a revert, an incident or lost data. Never merge to clear the queue.

## Release
For a `kind: release` task, these replace items 1 to 12. All are hard. R1 to R5 and R7 are for the merge: on a resume (a retry or a person's feedback after the deploy or an after-merge step stopped) the PR is already merged, so check only that it merged into `release_branch` with a merge commit and R6, then go on to the deploy.
- R1. `auto_merge: true` in the repo profile, or a person approved this release in `history.md`.
- R2. The PR is open, targets the profile's `release_branch`, its head branch was cut from the default branch (or wherever the profile's `## Release` says), and it is not `CONFLICTING`.
- R3. The PR head SHA is the SHA `04_preflight` passed, and `04_preflight/check.md` starts `pass`.
- R4. Every required CI check on that SHA is green.
- R5. The only commits on the branch that aren't on the default branch are the release commit(s), and they touch only the release files the profile's `## Release` names. Everything else shipping is already there.
- R6. The profile's `## Release` says how a merge reaches production (`deploy`, or `none`) and what follows it (`after merge`), so the release can be finished, not just merged.
- R7. Every check under its `before merge` holds.
