# 06_review - PR to panel verdict

One job: have specialists who did not write the code review the PR, and rule on it.

## Inputs
- Working (this run): `runs/{run}/tasks/{issue}/05_build/build.md` (PR URL, head SHA, worktree), `gh pr diff {pr} -R {repo}`, `gh issue view {issue} -R {repo}`
- Reference (every run): `stages/06_review/references/panel.md`, `skills/review-code/SKILL.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, `_shared/rules.md`, `_shared/confidence.md`

Do NOT load: `05_build/` beyond `build.md`, earlier attempts' review files, other tasks, the spec.

## Process
1. If `05_build/check.md` is not `pass`, stop and say so.
2. Pick the seats from `references/panel.md`.
3. Launch every seat in parallel as a fresh agent following `review-code` with its lens. Each writes `06_review/{seat}.md`.
4. Merge their findings into `verdict.md`: line 1 is the head SHA reviewed, then findings deduped and ordered Must, Should, Could.
5. Post it as one PR comment: `gh pr comment {pr} -R {repo} --body-file verdict.md`.

## Outputs
- `runs/{run}/tasks/{issue}/06_review/{seat}.md`, one per seat
- `runs/{run}/tasks/{issue}/06_review/verdict.md`

## Check
Apply the aggregation rule in `panel.md` and write `check.md` per `_shared/confidence.md`. `fail: retry - 05` sends `verdict.md` back to the builder; the runner caps the retries.
