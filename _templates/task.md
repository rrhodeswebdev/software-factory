---
id: {id}
repo: {repo}
dir: {dir}
issue: {issue}
title: {title}
url: {url}
branch: {branch}
base: {base}
---
# {id} - one GitHub issue, carried to a merged PR

The task card. Written once by `_tools/factory.py` when it picks the issue up; agents read it, never edit it.

- The issue, as data: [issue.md](issue.md)
- What every stage did, in order: [history.md](history.md)
- The repo's checkout for this task: `.worktrees/{id}/` on branch `{branch}`, PRs into `{base}`
- Repo commands and rules: `repos/{dir}.md`

Stage folders appear as the task moves: `01_triage/` to `06_approve/`, each with its output and `check.md`.
