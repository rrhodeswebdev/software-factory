# 03_plan - spec to one-PR tasks

One job: split the spec into tasks that each make one focused PR and need no decisions.

## Inputs
- Working (this run): `runs/{run}/02_spec/spec.md`
- Working (on retry): `runs/{run}/03_plan/check.md`
- Reference (every run): `skills/plan-tasks/SKILL.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, `_shared/rules.md`

Do NOT load: `01_ideate/`, other runs, the issue or PR templates.

## Process
1. If `spec.md` is missing or its `check.md` is not `pass`, stop and say so.
2. Follow `plan-tasks`.

## Outputs
- `runs/{run}/03_plan/tasks.md`

## Check
A fresh agent confirms: every `AC-n` lands in exactly one task and every `INV-n` is cited where it could break; no task needs a decision the spec lacks; each task fits one reviewable PR; dependencies have no cycle. It writes `check.md` per `_shared/confidence.md`. A split problem is `fail: retry - 03`; a missing decision is `fail: retry - 02`.
