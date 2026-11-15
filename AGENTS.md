# Software Factory

Takes an idea for any repo from brainstorm to deployed code with its GitHub issues closed. Agents do every step; a person is pulled in only when a check is not confident.

## Where things live

| Folder | What it holds |
|---|---|
| `stages/` | the eight stage contracts, in order; the pipeline on one screen: [CONTEXT.md](CONTEXT.md) |
| `runs/` | product: one folder per run, holding every stage's output and `check.md` |
| `repos/` | one profile per repo; each repo is a folder beside this one in the projects folder (`../{dir}`) |
| `skills/` | the factory's own skills, the how of each stage: [catalog](skills/CONTEXT.md) |
| `_shared/` | rules every stage reads: [rules](_shared/rules.md), [confidence gate](_shared/confidence.md) |
| `_templates/` | starters for a run, a repo profile, an issue and a PR |
| `_tools/` | `factory.py` runs stages as fresh agents, retries and notifies; `links.py` checks links and input paths |
| `setup/` | [onboard a repo](setup/onboard-repo.md), [run it on a schedule](setup/schedule.md) |

## Route by what just happened

| If | Go to | Then stop at |
|---|---|---|
| the repo folder has no profile in `repos/` | [onboard-repo](setup/onboard-repo.md) | the person approves the profile |
| a new idea for a repo | copy `_templates/run.md` to `runs/{YYYY-MM-DD}-{dir}-{slug}/RUN.md`, then [01_ideate](stages/01_ideate/CONTEXT.md) | 01's check |
| an issue labelled `factory:idea` | a new run with the issue as its idea (`factory.py pull` does this), then 01 | 01's check |
| "pull ready issues" for a repo | [05_build](stages/05_build/CONTEXT.md), pull mode | each task's 08 check |
| a `check.md` says `pass` | the next numbered stage | its check |
| a `check.md` says `fail: retry` | the stage that `check.md` names | its check |
| a `check.md` says `fail: human` | stop that task, report the why | a person edits `check.md` |
| a person gives notes on a stopped run or task | `python3 _tools/factory.py feedback {run} [{issue}] "{notes}"` | the stage's next check |
| a person drops a run or task | `python3 _tools/factory.py reject {run} [{issue}] "{why}"` | done |
| asked for status | `python3 _tools/factory.py status` | report what exists |
| asked to improve the factory | [lessons](_shared/lessons.md): fold each line into its skill or rule, then delete it | the person reviews the diff |
| resuming a run | the first stage folder in the run without a passing `check.md` | its check |

## How to run a stage

Use only the factory's own `skills/`, nothing installed elsewhere. Give a fresh agent only the stage's `CONTEXT.md`, the run id, and for stages 05–08 the issue number. The orchestrating agent reads nothing but the first line of each `check.md`. Stages 01–04 run once per run; 05–08 run once per task, independent tasks in parallel, dependent tasks in order.

## The one rule

Nothing moves on until the last stage's `check.md` says `pass`.
