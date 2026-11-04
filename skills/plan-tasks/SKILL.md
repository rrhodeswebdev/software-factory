---
name: plan-tasks
description: Software factory stage 03. Splits an approved spec into ordered tasks that each become one focused pull request a fresh agent can finish without making decisions.
---
# plan-tasks - one task, one PR, no decisions left

## Rules
- Split by working result someone can observe, not by layer or file. "Add a column" is only a task when other tasks depend on it.
- A task fits one reviewable PR: roughly under 400 changed lines, not counting tests and generated files. Bigger means split.
- Each shared contract (schema, API shape, shared type) is defined in exactly one task; the tasks that use it depend on that one.
- A refactor needed first is its own task and changes no behavior.
- Every `AC-n` lands in exactly one task. Every `INV-n` is cited in each task that could break it.
- Order by dependency and keep the chains short, so most tasks can run in parallel.
- Copy into each task the spec decisions it needs. Its GitHub issue must stand alone, because builders never see the spec.

## Task shape
```
## T{n} - {title}
Outcome: {what works after this, in one or two sentences}
Acceptance criteria:
- AC-{n}: {copied with its ID}
Invariants to keep: INV-{n}, ...
Decisions this task needs: {copied in full}
Touches: {files or areas, best guess}
Depends on: T{n} | nothing
Out of scope: {what a builder might be tempted to add}
```
