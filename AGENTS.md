# Software Factory

A personal factory that takes GitHub issues labelled `factory` in any onboarded repo and carries each to a merged pull request. Specialist agents do every step, several tasks at once; a person is asked only when a check isn't confident.

## Where things live

| Folder | What it holds |
|---|---|
| `stages/` | the six stage contracts, in order; the pipeline on one screen: [CONTEXT.md](CONTEXT.md) |
| `stages/05_review/lenses/` | one file per specialist reviewer: code, security, performance, ui-ux, accessibility, tests, simplicity, data |
| `tasks/` | product: one folder per task, with each stage's output, `check.md` and `history.md`: [shelf](tasks/CONTEXT.md) |
| `repos/` | one profile per repo; each repo is a folder beside this one (`../{dir}`): [shelf](repos/CONTEXT.md) |
| `skills/` | skills for the person driving the factory: [catalog](skills/CONTEXT.md) |
| `_shared/` | what every agent reads: [rules](_shared/rules.md), [history and handoffs](_shared/history.md) |
| `_templates/` | starters for a task card, a repo profile, an issue and a PR |
| `.claude/agents/` | one agent per job, each with its own model and tools |
| `_tools/` | `factory.py` runs everything; `dashboard.py` shows it; `links.py` checks links |
| `setup/` | [keep it running](setup/schedule.md) |

## Route by what just happened

| If | Do | Then stop at |
|---|---|---|
| a repo folder has no profile in `repos/` | the [onboard-repo](skills/onboard-repo/SKILL.md) skill | the person approves the profile |
| a person has a task in mind | the [new-task](skills/new-task/SKILL.md) skill, or `python3 _tools/factory.py new {dir} "{title}" "{details}"` | the issue exists |
| "work on tasks", start, stop or check the factory | the [factory](skills/factory/SKILL.md) skill (`/factory start`) | each task's last check |
| a task stopped for a person | the [unblock](skills/unblock/SKILL.md) skill | the person's choice is applied |
| asked what is happening | `/factory status`, or `/factory dashboard` | report what exists |
| you are a stage agent | your stage's `CONTEXT.md` and [rules](_shared/rules.md), nothing else | your `check.md` |

## The one rule

Nothing moves on until the last stage's `check.md` says `pass`, and nothing merges unless the [gate](stages/06_approve/references/gate.md) holds.
