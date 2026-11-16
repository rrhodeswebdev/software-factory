---
id: {id}
repo: {repo}
dir: {dir}
issue: {issue}
title: {title}
url: {url}
branch: {branch}
base: {base}
kind: {kind}
---
# {id} - one GitHub issue, carried to a merged PR

The task card. Written once by `_tools/factory.py` when it picks the issue up; agents read it, never edit it.

- The issue, as data: [issue.md](issue.md)
- What every stage did, in order: [history.md](history.md)
- The repo's checkout for this task: `.worktrees/{id}/` on branch `{branch}`, PRs into `{base}`
- Kind: `{kind}`. A `release` merges the default branch's new work into `{base}` and runs only `03_build`, `04_preflight` and `06_approve`
- Repo commands and rules: `repos/{dir}.md`

Stage folders appear as the task moves: `01_triage/` to `06_approve/`, each with its output and `check.md`.
