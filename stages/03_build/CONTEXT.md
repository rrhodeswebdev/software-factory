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
4. Prove each AC with a test that would fail if the behavior broke; run it and keep the output. For `UI: yes`, also start the dev server and check the change in a real browser if you have one; record what you saw.
5. Run the profile's lint, typecheck, test and build commands until they pass.
6. Commit with clear messages ending `Refs #{issue}`. Push: `git push -u origin {branch}`. Never push to the base branch.
7. No PR yet: `gh pr create --draft --base {base} --head {branch}` with a title naming the change and a body from `_templates/pr.md`. A PR already open: push to it and update its body's Proof table.

## Outputs
- The pushed branch and the draft PR.
- `tasks/{id}/03_build/build.md`: first the line `PR: <full PR URL>`, then the head commit SHA, what changed, a table AC → proof (test name + command + result), and on a retry `## Findings answered`: each finding → fixed (how) or disputed (why).
- `tasks/{id}/03_build/check.md`: `pass`, `fail: retry 02 - <spec gap>`, or `fail: human - <why>`.
- A handoff appended to `tasks/{id}/history.md`.

## Check
04_preflight reruns every command on the pushed commit, and 05_review reads the diff against the spec. The builder never judges its own work final.
