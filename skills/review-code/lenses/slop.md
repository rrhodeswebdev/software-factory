# Lens: slop - every line must earn its place

Each finding must show the simpler version that keeps the same behavior and proof.

- Dead code: unused functions, exports, params, branches, files, dependencies.
- An abstraction, wrapper, interface or factory with one caller and no second in sight.
- Options, flags or config nobody asked for; "for later" hooks.
- Defensive checks for states the types or callers already rule out.
- Logic that duplicates a helper already in the repo (cite the helper).
- Comments that restate the code; filler in comments, docs or the PR body ("robust", "seamless", "comprehensive").
- Commented-out code, leftover debug logs, stray TODOs.
- Catch-and-rethrow that adds nothing; casts that hide type errors.
- Tests that only assert on mocks, or repeat the implementation.

Findings at confidence 4 or more count as Should fix: removing slop is this seat's job.
