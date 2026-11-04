# 02_spec - brief to testable spec

One job: settle every behavior, interface and data decision so no builder has to invent one.

## Inputs
- Working (this run): `runs/{run}/01_ideate/idea.md`
- Working (on retry): `runs/{run}/02_spec/review.md` and `runs/{run}/02_spec/check.md`
- Reference (every run): `skills/write-spec/SKILL.md`; for the check, `skills/review-spec/SKILL.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, and the target repo's code at the profile's `path:`
- Reference (every run): `_shared/rules.md`, `_shared/confidence.md`

Do NOT load: other runs, `03_plan/` onward.

## Process
1. If `idea.md` is missing or its `check.md` is not `pass`, stop and say so.
2. Follow `write-spec`. A decision you cannot make at confidence 4 or more stops the run with `fail: human`.
3. On retry, fix only what `review.md` raised.

## Outputs
- `runs/{run}/02_spec/spec.md`

## Check
A fresh agent follows `review-spec`, writes `02_spec/review.md`, and writes `check.md` per `_shared/confidence.md`: `pass` if no Must fix or Should fix at confidence 4 or more. On `fail: retry`, rerun 02.
