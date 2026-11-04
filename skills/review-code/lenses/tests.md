# Lens: tests - would the tests catch it if this broke

- Every `AC-n` and cited `INV-n` has proof in the PR's proof table, and that proof exists in the diff or the run.
- Each core test fails when the behavior breaks. When it is cheap, break the code and run it.
- Assertions are on what a user or caller observes, not on internals or mock calls.
- The unit under test is not mocked; only outside boundaries are.
- Failure paths and edge cases from the issue are tested, not only the happy path.
- Flaky patterns: sleeps, real clocks, real network, order dependence, shared state between tests.
- Snapshot-only tests standing in for real assertions.
