# 04_issues - tasks to GitHub issues

One job: file each task as a self-contained GitHub issue and open a folder for it.

## Inputs
- Working (this run): `runs/{run}/03_plan/tasks.md`
- Reference (every run): `_templates/issue.md`, `_shared/rules.md`, `runs/{run}/RUN.md` (the `repo:` line)

Do NOT load: `spec.md` (the tasks already carry what the issues need), other runs.

## Process
1. If `tasks.md` is missing or its `check.md` is not `pass`, stop and say so.
2. Skip tasks already filed: `gh issue list -R {repo} --label factory --search "{run} in:body"`.
3. In dependency order, fill `_templates/issue.md` for each task, swapping each `T{n}` dependency for its issue number, and run `gh issue create -R {repo} --title "{title}" --body-file {file} --label factory --label factory:ready`.
4. Create `runs/{run}/tasks/{issue}/` for each issue.

## Outputs
- `runs/{run}/04_issues/issues.md`: one table row per task, exactly `| T1 | #123 | {url} |` (the runner reads it)

## Check
For every row, `gh issue view {issue} -R {repo} --json state,labels` shows it open and labelled; the row count equals the task count. Write `check.md` per `_shared/confidence.md`. On `fail: retry`, rerun 04 (step 2 keeps it from filing twice).
