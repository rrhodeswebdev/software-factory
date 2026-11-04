---
name: write-spec
description: Software factory stage 02. Turns a decided brief into a spec with numbered acceptance criteria, invariants and settled decisions, so no builder has to invent anything.
---
# write-spec - from a brief to a spec a builder cannot misread

Goal: every decision that changes behavior, interfaces, data, security, operations or proof is made here, not during the build.

## Method
1. Read the brief, the target repo's entry docs, and the code the change will touch: data models, APIs, routes, screens, existing tests. Name the files. Reuse the repo's existing patterns.
2. List every decision the build depends on. For each, make the call and write one line on why and one on the rejected option. If your confidence in a call is below 4 (scale in `_shared/confidence.md`), do not guess: it is a question for a person.
3. Write each acceptance criterion as behavior someone can observe: `AC-n: When {actor} {does X}, {observable result}.` Each must be provable by a test or a command someone can run.
4. Write invariants for what must stay true: existing behavior that must not break, security properties. `INV-n: {what stays true}.`
5. Give every criterion that takes input or calls something its failure path: bad input, missing permission, dependency down.
6. For data changes, state the schema change, migration, backfill, and whether it destroys or rewrites existing data (that is always human).
7. Give a proof plan: for each criterion, the kind of proof (unit, integration, end-to-end, browser).

## Spec shape (routine features ~600–1000 words; longer only where a decision needs it)
```
# {feature} - spec
## Summary
## Users and flows
## Acceptance criteria
## Invariants
## Decisions        (decision | choice | why | rejected)
## Interfaces and data
## Failure handling
## Security and privacy
## Proof plan
## Out of scope
## Open questions   (non-blocking only, each with its default)
```
