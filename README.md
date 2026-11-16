# Software Factory

A personal software factory for any repo. Label a GitHub issue `factory`, or file one through the factory, and specialist Claude Code agents carry it to a merged pull request: triage, spec, build, preflight, a review panel picked for the change, and a final approver that merges or asks you. Several tasks run at once, each in its own git worktree, and every task keeps a history every agent reads before it starts.

The whole factory is this folder: plain markdown contracts, agent definitions and two standard-library Python scripts. Repos it works on sit beside it.

## Needs
- [Claude Code](https://docs.claude.com/en/docs/claude-code), signed in
- [GitHub CLI](https://cli.github.com/) (`gh auth login`)
- Python 3.10+, git, macOS (for notifications; everything else is portable)

## Start
```sh
cd ~/projects/software-factory
claude                                   # then: /onboard-repo myapp  (writes repos/myapp.md)
python3 _tools/factory.py new myapp "Add CSV export" "## Done when
- the Reports page has an Export CSV button"
python3 _tools/factory.py watch          # works every open factory issue, pulls every 5 min
python3 _tools/dashboard.py              # http://127.0.0.1:8787
```

## How it works
Read [AGENTS.md](AGENTS.md) for the map and [CONTEXT.md](CONTEXT.md) for the pipeline. In short:

| Stage | Agent | Job |
|---|---|---|
| 01 triage | `factory-triage` | is it worth doing, already done, clear, one PR? |
| 02 spec | `factory-spec` | testable acceptance criteria, settled decisions |
| 03 build | `factory-builder` | the change, the proof, a draft PR |
| 04 preflight | `factory-preflight` | install, lint, typecheck, test, build, CI |
| 05 review | `factory-orchestrator` + `factory-reviewer` ×n | code, security, performance, ui-ux, accessibility, tests, simplicity, data; only the lenses a change needs |
| 06 approve | `factory-approver` | walks the merge gate: merges, or asks you |

When a task stops for you, the issue is labelled `factory:needs-human`, you get a notification, and the dashboard lists it. Merge or close the PR on GitHub, or use `/unblock` in Claude Code.

## Safety
Agents run unattended (`bypassPermissions`). The guards: only issues a person labelled `factory` are taken; issue text is treated as data; agents may not change the factory's own files (the runner checks and stops the task); only the approver merges, and only when [the gate](stages/06_approve/references/gate.md) holds; protected paths always go to a person. Set `auto_merge: false` in a repo's profile to approve every merge yourself.

MIT licensed.
