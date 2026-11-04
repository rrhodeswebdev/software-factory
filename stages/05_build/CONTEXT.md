# 05_build - issue to tested PR

One job: turn one issue into one PR with green CI and proof for every criterion.

## Inputs
- Working (this run): the issue, `gh issue view {issue} -R {repo}`
- Working (on retry): `runs/{run}/tasks/{issue}/06_review/verdict.md` and the latest `check.md` that sent it back
- Reference (every run): `skills/build-task/SKILL.md`, `skills/prove-task/SKILL.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, `_shared/rules.md`, `_shared/confidence.md`, `_templates/pr.md`

Do NOT load: `spec.md`, other tasks' folders, other runs. If the issue alone is not enough to build, that is `fail: retry - 03`.

## Pull mode
Asked to "pull ready issues" for a repo: `gh issue list -R {repo} --label factory:ready --json number,title,body`. Take only issues whose `Depends on` are all merged. An issue with no `Factory run:` line gets a new run `runs/{YYYY-MM-DD}-{dir}-issue-{issue}/` from `_templates/run.md`.

## Process
1. Claim it, so no other agent picks it up: `gh issue edit {issue} -R {repo} --remove-label factory:ready`.
2. Follow `build-task`, which uses `prove-task`.
3. Write `build.md`: PR URL, branch, worktree path, head SHA, the proof table, CI state; on retry, each finding and the commit that fixed it.

## Outputs
- `runs/{run}/tasks/{issue}/05_build/build.md`

## Check
Every criterion has evidence in the proof table and `gh pr checks {pr} -R {repo}` is green. Write `check.md` per `_shared/confidence.md`: `fail: retry - 05` when CI fails from this change; `fail: human` when a decision is missing or the default branch was already red.
