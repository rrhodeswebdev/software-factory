---
name: review-spec
description: Software factory stage 02 check. A fresh agent reviews a spec for gaps, contradictions and risks before any task is planned.
---
# review-spec - catch spec gaps while they are cheap

Goal: find what would make a builder guess, or make the shipped change wrong or unsafe. You did not write this spec.

## Look for
- An acceptance criterion that is not observable or not testable.
- A decision left to the builder ("handle errors appropriately", "use a suitable store").
- Sections that contradict each other, or contradict the existing code.
- An outcome in the brief that no acceptance criterion covers; anything in the spec the brief did not ask for.
- A missing failure path: bad input, no permission, dependency down, retry or double submit.
- Security: authentication and per-object authorization on every new endpoint or screen, input validation at trust boundaries, secrets, personal data in responses or logs.
- Data: a destructive migration, no backfill, no way back.
- A criterion the proof plan cannot actually prove.

## Report
Write findings in the format from [review-code](../review-code/SKILL.md), in priority order, into `review.md`. Read enough of the code to back each finding. End with `Verdict: Approve | Request changes | Blocked` and what you could not verify.
