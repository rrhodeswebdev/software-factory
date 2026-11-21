# 03_build - one PR that meets the spec

One job: make the change in the task's worktree, prove every acceptance criterion, and open (or update) one pull request.

Agent: `factory-builder`. Paths are from the factory root; you work inside the worktree named in your prompt, on its branch.

## Inputs
- Working (this task): `tasks/{id}/02_spec/spec.md`, `tasks/{id}/history.md`
- Working (on a retry): `tasks/{id}/04_preflight/preflight.md` and `tasks/{id}/05_review/` (one `<seat>.md` per reviewer): the failures and findings to fix
- Reference (every task): `_shared/rules.md`, `_shared/history.md`
- Reference (every task): `repos/{dir}.md`, `_templates/pr.md`

Do NOT load: other tasks, triage notes the spec already absorbed.

## Process
1. Read `history.md` and `spec.md`. If the spec can't be built without guessing, stop: `fail: retry 02 - <the gap>`.
2. On a retry, list every failure from preflight and every `blocking` and `should` finding from review. Fix each, or dispute it with evidence. A finding you neither fix nor dispute fails the next review.
3. Build the smallest change that meets every AC and keeps every INV. Follow the repo's own guide.
4. Prove each AC with a test that would fail if the behavior broke; run it and keep the output. For `UI: yes`, also start the dev server and check the change in headless Chromium (Playwright is installed); for a native app, in the iOS simulator (`xcrun simctl`). Record what you saw. Skip a check only when it needs what you can't have (a physical device, a real payment), and say so in `build.md`.
5. Run the profile's lint, typecheck, test and build commands until they pass.
6. Commit with [Conventional Commit](../../_shared/rules.md) messages (`feat(404): link each home section`), each ending `Refs #{issue}`. Push: `git push -u origin {branch}`. Never push to the base branch.
7. No PR yet: `gh pr create --draft --base {base} --head {branch}` with a Conventional Commit title naming the change (`fix(nav): ...`; `feat` only for something a user can now do) and a body from `_templates/pr.md`. A PR already open: push to it and update its body's Proof table.

## Outputs
- The pushed branch and the draft PR.
- `tasks/{id}/03_build/build.md`: first the line `PR: <full PR URL>`, then the head commit SHA, what changed, a table AC → proof (test name + command + result), and on a retry `## Findings answered`: each finding → fixed (how) or disputed (why).
- `tasks/{id}/03_build/check.md`: `pass`, `fail: retry 02 - <spec gap>`, or `fail: human - <why>`.
- A handoff appended to `tasks/{id}/history.md`.

## Check
04_preflight reruns every command on the pushed commit, and 05_review reads the diff against the spec. The builder never judges its own work final.

## A release task
`kind: release` in `TASK.md`: the PR ships the default branch to `{base}`, the profile's `release_branch`. There is no spec; every change in it was reviewed on its way into the default branch. Instead of Process steps 1 to 5:
1. Read the profile's `## Release` and the repo's own release guide. The profile has no `release_branch`, or the issue title names no version: `fail: human - <what's missing>`.
2. The issue names a `Source:` SHA (`factory.py release` writes it): on the first attempt, `git reset --hard <sha>` so the release ships exactly what its version was counted from; newer work waits for the next release. Nothing to ship (`git log origin/{base}..HEAD` is empty): `fail: human - nothing to release`.
3. Make the release commit exactly as `## Release` says (its `release files`: a version bump, a changelog), and nothing else. Run the profile's lint and build.
4. Commit with the repo's release message (`chore(release): {version}` if its guide names none) ending `Refs #{issue}`, push, and open the PR as in step 7 with base `{base}`. Its body lists what ships (`git log --no-merges --format='- %s' origin/{base}..HEAD`) and says merging deploys to production.

`build.md` holds the PR line, the head SHA, the version and the list of what ships; there is no AC table.
