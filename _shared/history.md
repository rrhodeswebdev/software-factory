# History - how agents hand a task to each other

Each task keeps one timeline, `tasks/{id}/history.md`. It is the factory's memory: an agent starting cold reads it and knows what was done, what was decided and what is still open, without rereading every output.

## Who writes what
- **The runner** appends one-line events: `- 2026-11-15 20:31 · 03_build started (attempt 2)`, each verdict, the review panel.
- **A person** appends `## Feedback from a person` sections through `factory.py feedback`. They outrank every handoff.
- **Each stage agent** appends one handoff section before it stops. Review seats and the orchestrator don't: the runner logs the panel's verdict, and their findings files are the record.

## The handoff
Append, never rewrite earlier entries. At most twelve lines; detail lives in your stage's output files, so link them.

```markdown
## 03_build · factory-builder · attempt 2 · 2026-11-15 20:44
- Did: fixed the two blocking findings from security.md; PR #31 now at a1b2c3d
- Decided: kept the old cache key format so existing sessions survive (spec INV-1)
- Disputed: performance.md finding 2, see build.md "Findings answered"
- Open: none
- For next: preflight should rerun `bun run build`; the lockfile changed
- Output: 03_build/build.md
```

`Did` and `Output` are required. Add `Decided`, `Disputed`, `Open` and `For next` when they hold something; skip them when they don't.
