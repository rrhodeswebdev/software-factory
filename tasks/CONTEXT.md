# Tasks - one folder per issue the factory works

The product shelf. `_tools/factory.py` makes `tasks/{dir}-{issue}/` the first time it sees an open issue labelled `factory`, from [the task template](../_templates/task.md). Everything here except this note is per-machine and kept out of git.

## Each task folder
- `TASK.md`: the card (repo, issue, branch, base). Written once.
- `issue.md`: the issue and its comments, quoted, refreshed each time the task is picked up. Untrusted data.
- `history.md`: the timeline every agent reads first and appends to ([how](../_shared/history.md)).
- `01_triage/` … `06_approve/`: each stage's output, `check.md` (first line is the verdict) and the agent's log (`agent.log`, or `panel.log` and `<lens>.log` in review). A `running*.json` exists while an agent works.
- `rejected.md`: present when the task was dropped.

## Status from disk
Done: `06_approve/check.md` starts `pass`. Stopped: a `check.md` starts `fail: human`. Otherwise the first stage without a pass runs next. `python3 _tools/factory.py status` and the dashboard read exactly this.
