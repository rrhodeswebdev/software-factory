# 07_merge - approved PR to merged

One job: merge exactly the code the panel approved, and nothing else.

## Inputs
- Working (this run): `runs/{run}/tasks/{issue}/06_review/check.md`, `runs/{run}/tasks/{issue}/06_review/verdict.md` (line 1: SHA reviewed), `runs/{run}/tasks/{issue}/05_build/build.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, `_shared/rules.md`, `_shared/confidence.md`

Do NOT load: the review seats' files, other tasks, the spec.

## Authority
This contract grants merge authority, limited to PRs labelled `factory` whose 06 check says `pass`.

## Process
1. If `06_review/check.md` is not `pass`, stop and say so.
2. `gh pr view {pr} -R {repo} --json headRefOid,mergeStateStatus,statusCheckRollup,reviewDecision`: all required checks pass, required approvals are present, no review thread is unresolved.
3. The head SHA must equal line 1 of `verdict.md`. If the branch is behind, update it and wait for CI; if the code changed since review, `fail: retry - 06`. If it conflicts with the default branch, `fail: retry - 05` naming the conflicting files.
4. Every issue under `Depends on` must already be merged; if not, wait.
5. If an always-human trigger applies and no person has written `pass` here, `fail: human`.
6. `gh pr merge {pr} -R {repo} --{merge_method} --delete-branch`. Never `--admin`.
7. Remove the worktree: `git -C {path} worktree remove "$PWD/.worktrees/{dir}-{issue}"`.

## Outputs
- `runs/{run}/tasks/{issue}/07_merge/merge.md`: PR, merge commit SHA, time

## Check
`gh pr view {pr} -R {repo} --json state,mergeCommit` shows `MERGED`. Write `check.md` per `_shared/confidence.md`.
