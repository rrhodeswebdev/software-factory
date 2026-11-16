# Pipeline - one issue to one merged PR

Every task runs the same six stages. `_tools/factory.py` is the conveyor: it picks issues up, gives each task its own git worktree, runs each stage as a fresh agent, routes on the first line of each `check.md`, and runs many tasks at once (`FACTORY_AGENTS`, default 4 agents at a time).

```
GitHub issue labelled `factory`
  │
  01_triage      factory-triage        worth doing?          pass │ reject │ human
  02_spec        factory-spec          what done looks like  pass │ human
  03_build       factory-builder       change + proof + PR   pass │ retry 02 │ human
  04_preflight   factory-preflight     lint, build, CI green pass │ retry 03 │ human
  05_review      factory-orchestrator  picks the panel, then
                 factory-reviewer ×n   one seat per lens     pass │ retry 03
  06_approve     factory-approver      the merge gate        merged │ retry 03/04 │ human
  │
merged PR, issue closed
```

| Stage | Contract | Writes |
|---|---|---|
| 01 | [triage](stages/01_triage/CONTEXT.md) | `triage.md` |
| 02 | [spec](stages/02_spec/CONTEXT.md) | `spec.md` |
| 03 | [build](stages/03_build/CONTEXT.md) | branch, draft PR, `build.md` |
| 04 | [preflight](stages/04_preflight/CONTEXT.md) | `preflight.md` |
| 05 | [review](stages/05_review/CONTEXT.md) | `panel.md`, `<lens>.md` per seat |
| 06 | [approve](stages/06_approve/CONTEXT.md) | `approval.md`, the merge |

## Routing
- `pass`: the next stage runs.
- `fail: retry NN`: stage `NN` runs again with the reason in `history.md`; later stages rerun after it. A stage that runs three times without a pass stops for a person.
- `fail: human`: the task stops. The issue gets `factory:needs-human` and a comment; macOS notifies; the dashboard lists it. A person merges or closes the PR on GitHub, or runs `feedback` or `reject`.
- `reject` (triage only): the issue gets the reason and `factory:rejected`.

## Labels
`factory` (take this), `factory:working`, `factory:needs-human`, `factory:rejected`. Removing `factory` pauses a task. `Depends on: #12` in an issue holds it until #12 is closed.

## Memory
Each task's [history](_shared/history.md) is the thread between agents: runner events, every stage's handoff, a person's feedback.
