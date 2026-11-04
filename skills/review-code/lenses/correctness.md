# Lens: correctness - does it do what the issue says, without breaking anything

- Go criterion by criterion: does the code make each `AC-n` true, including its failure path?
- Edge cases: empty, null, zero, one, many, duplicates, unicode, time zones and DST, rounding with money.
- Races: double submit, concurrent writes, retries that are not idempotent, stale reads.
- Errors swallowed, logged and ignored, or turned into a wrong success.
- Existing callers: changed signatures, return shapes, defaults, or API responses that break them.
- Migrations: safe on the existing data, reversible, ordered correctly against the deploy.
- The decisions copied into the issue: followed, not reinterpreted.
- Scope: changes the issue did not ask for.
