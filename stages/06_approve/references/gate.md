# Gate - what must hold before the factory merges on its own

The approver's checklist. Every item must hold. Items marked ◆ are judgment: a person's written approval in `history.md` can stand in for them. The others are hard facts nothing replaces.

## Hard
1. `auto_merge: true` in the repo profile, or a person approved this merge in `history.md`. With `false`, only a person's approval lets the factory merge.
2. The PR is open, targets the profile's `default_branch`, and is not `CONFLICTING`.
3. The PR head SHA is the SHA `04_preflight` passed and the worktree `HEAD` the panel reviewed. Nothing was pushed after.
4. Every required CI check on that SHA is green. None pending, none skipped that is required.
5. `04_preflight/check.md` and `05_review/check.md` both start `pass`.
6. The diff touches no protected path: the profile's `## Protected paths`, plus always `.github/workflows/`, `.env*`, secrets and credentials files, and CI or deploy config.

## Judgment ◆
7. Every AC in `spec.md` has proof in `build.md` you can trace: a named test that exists in the diff or the repo, and a result. Every INV still holds.
8. Every `should` finding is fixed or disputed in `build.md`, and each dispute convinces you.
9. The change is about one concern and under about 600 changed lines, not counting lockfiles and generated files.
10. No new dependency unless the spec asked for one, and no lockfile change without a reason.
11. It doesn't touch authentication, authorization, payments, data migrations or deletes of user data. If it does, a person looks, however clean it reads.
12. You can say in two sentences what the change does and why it is safe. If you can't, you are not confident.

## When unsure
Ask. A person costs minutes; a bad merge costs a revert, an incident or lost data. Never merge to clear the queue.
