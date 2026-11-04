# Software Factory - the pipeline

The flow: decide it, spec it, split it, file it, build it, review it, merge it, ship it.

| Stage | Job | Runs |
|---|---|---|
| [01_ideate](stages/01_ideate/CONTEXT.md) | raw idea to decided brief | once per run |
| [02_spec](stages/02_spec/CONTEXT.md) | brief to spec with `AC-n` IDs | once per run |
| [03_plan](stages/03_plan/CONTEXT.md) | spec to one-PR tasks | once per run |
| [04_issues](stages/04_issues/CONTEXT.md) | tasks to GitHub issues | once per run |
| [05_build](stages/05_build/CONTEXT.md) | issue to tested PR | per task |
| [06_review](stages/06_review/CONTEXT.md) | PR to specialist-panel verdict | per task |
| [07_merge](stages/07_merge/CONTEXT.md) | approved PR to merged | per task |
| [08_deploy](stages/08_deploy/CONTEXT.md) | merged to deployed, issue closed | per task |

Factory (every run): `_shared/`, `skills/`, the repo's profile in `repos/`, `_templates/`, each stage's `references/`.
Code: each repo is a folder beside the factory (`../{dir}`); builds happen in worktrees under `.worktrees/`.
Product (new each run): `runs/{run}/`, shaped like this:

```
runs/2026-11-03-cheergenics-team-chat/
  RUN.md                           repo + profile link (from _templates/run.md)
  01_ideate/idea.md   check.md
  02_spec/spec.md     review.md  check.md
  03_plan/tasks.md    check.md
  04_issues/issues.md check.md
  tasks/123/05_build/build.md      check.md
  tasks/123/06_review/<specialist>.md  verdict.md  check.md
  tasks/123/07_merge/merge.md      check.md
  tasks/123/08_deploy/deploy.md    check.md
```

**Broken on purpose:** outputs do not live in `stages/*/output/`. Runs for different repos happen at the same time, so each run keeps its own stage folders under `runs/`, and `stages/` holds only contracts.

**Fan-out:** at 04 one run becomes N tasks, and 05–08 run once per task. Entering at 05 (pull mode) works for any issue labelled `factory:ready`, whether the factory filed it or a person did.

**Running it:** `python3 _tools/factory.py new {dir} "{idea}"` drives a run end to end, each stage a fresh headless Claude Code process with a time limit; `resume {run}` continues one; `pull` builds every `factory:ready` issue and runs on a schedule ([setup/schedule.md](setup/schedule.md)). To shape the idea with an agent yourself, do 01 in a chat, then `resume`.

**Status:** a stage is done when its folder holds its output and a `check.md` whose first line is `pass`. A run is done when every task's 08 check passes.

**Self-contained:** every stage follows a skill in `skills/` and nothing installed outside this folder. Skills are plain markdown, so any agent that reads files can run them; Claude Code also lists them as slash commands through `.claude/skills`.
