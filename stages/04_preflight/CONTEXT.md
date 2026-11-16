# 04_preflight - is the PR ready for review

One job: prove the pushed commit installs, lints, typechecks, tests and builds, and that CI agrees, before any reviewer spends time on it.

Agent: `factory-preflight`. Run commands inside the task's worktree.

## Inputs
- Working (this task): `tasks/{id}/03_build/build.md`, `tasks/{id}/history.md`
- Reference (every task): `_shared/rules.md`, `_shared/history.md`
- Reference (every task): `repos/{dir}.md` (its Commands and CI sections are your checklist)

Do NOT load: the spec, review lenses, other tasks. You check readiness, not design.

## Process
1. `git fetch origin` and confirm the worktree's `HEAD` is the PR's head (`gh pr view <PR> --json headRefOid`). If not, `fail: retry 03 - worktree and PR differ`.
2. Run, in order, each profile command that isn't `none`: install, format/lint auto-fix, lint check, typecheck, test, build. Record command, exit code and, on failure, the first error lines.
3. Auto-fix only what a formatter or `--fix` linter changes on its own. Commit that as `chore: format`, push, and say so. Never hand-edit code here.
4. Scan the diff (`git diff origin/{base}...HEAD`) for conflict markers, debug leftovers (`console.log`, `debugger`, `print(` added for debugging, `.only(`), committed secrets or `.env` files, and files unrelated to the spec. Check every commit subject on the branch (`git log --no-merges --format=%s origin/{base}..HEAD`) and the PR title are Conventional Commits; any that aren't is `fail: retry 03 - not a conventional commit: <subject>`.
5. Check the PR: `gh pr view <PR> --json mergeable` is not `CONFLICTING`; `gh pr checks <PR> --watch --interval 30` (give up after 20 minutes) ends with every required check green.
6. If a command fails, run it on the base too, in a throwaway checkout: `git worktree add --detach <worktree>-base origin/{base}`, run it there, then `git worktree remove --force <worktree>-base`. Failing on base too is the repo's problem, not the builder's: `fail: human`.

## Outputs
- `tasks/{id}/04_preflight/preflight.md`: the head SHA, one row per command (exit code, time), the diff scan, the CI result.
- `tasks/{id}/04_preflight/check.md`: `pass - <sha>`, `fail: retry 03 - <command>: <first error>` (or the conflict, or the scan hit), or `fail: human - <why>`.
- A handoff appended to `tasks/{id}/history.md`.

## Check
The commands' exit codes and CI's result are the check: this stage reports them, it doesn't judge them. Its `pass` names the SHA every reviewer and the approver must see unchanged.

## A release task
`kind: release` in `TASK.md`: the diff against `{base}` is every change since the last release, not one spec's. Run every step; in the step 4 scan, skip "files unrelated to the spec", apply the conventional-commit check on the release commit and PR title only (earlier commits shipped already), and also check that the only commits on the branch not already on the default branch are the release commit(s) the profile's `## Release` describes.
