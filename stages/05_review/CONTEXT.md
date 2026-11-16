# 05_review - a panel of specialist reviewers

One job: the right specialists read the PR at once, each through one lens, and report only real, evidenced problems.

Two kinds of agent work here, both launched by the runner: the orchestrator picks the panel, then one `factory-reviewer` per seat runs in parallel. The runner writes `check.md` from the seats' first lines. Your prompt says which part is yours.

## Inputs
- Working (this task): `tasks/{id}/02_spec/spec.md`, `tasks/{id}/03_build/build.md`, `tasks/{id}/04_preflight/preflight.md`, `tasks/{id}/history.md`
- Working (this task): the worktree; the change is `git diff origin/{base}...HEAD`
- Reference (every task): `_shared/rules.md`
- Reference (every task): `stages/05_review/lenses/` (one file per lens: when it sits, what it looks for, its model)

Do NOT load: other tasks, lenses that aren't yours (seats), the 01 triage notes.

## Panel
For `factory-orchestrator`.
1. Read `spec.md`, then `git diff --stat origin/{base}...HEAD` and skim the diff.
2. Read only the frontmatter `use when:` line of each lens in `stages/05_review/lenses/`.
3. Pick every lens whose `use when` this change meets. `code` always sits. Fewer, sharper seats beat a full bench: a one-line copy fix needs `code` alone; a new form with an API call may need `code`, `security`, `ui-ux`, `accessibility` and `tests`.
4. Write `tasks/{id}/05_review/panel.md`: one line per seat, `- <lens>: <why this change needs it>`, then stop. No handoff.

## Seat
For `factory-reviewer`, one lens each.
1. Read your lens file, `spec.md`, `build.md`, then the full diff and the code it connects to (callers, tests, config).
2. If an earlier round's findings appear in `history.md` or `build.md` `## Findings answered`, check each fix landed and each dispute holds.
3. Report only what you can show: `file:line`, what goes wrong, the input or scenario that triggers it, and the fix. No style preferences the repo's linter doesn't enforce; no "consider" without a concrete failure.
4. Rate each: **blocking** (wrong, unsafe or breaks an AC/INV: must fix before merge), **should** (a real cost, fix now unless disputed), **note** (worth knowing, no action).
5. Write `tasks/{id}/05_review/<lens>.md`. First line: `pass` when nothing is blocking, else `fail: <n> blocking`. Then the findings, most severe first, or "No findings." Then stop. No handoff: the runner logs the panel's verdict.

## Outputs
- `tasks/{id}/05_review/panel.md` (orchestrator), `tasks/{id}/05_review/<lens>.md` (each seat)
- `tasks/{id}/05_review/check.md`, written by the runner: `pass - <seats>` or `fail: retry 03 - blocking findings from <seats>`

## Check
The runner reads each seat's first line: any `fail` sends the task back to 03 with the findings; three rounds without a clean panel stop it for a person. The approver reads every finding again before merging.
