# 06_approve - merge, or ask a person

One job: merge the PR when every item of the gate holds and you are confident; otherwise hand it to a person with exactly what to look at.

Agent: `factory-approver`. The runner lets only one approver work per repo at a time.

## Inputs
- Working (this task): `tasks/{id}/TASK.md`, `tasks/{id}/history.md`, `tasks/{id}/02_spec/spec.md`, `tasks/{id}/03_build/build.md`, `tasks/{id}/04_preflight/preflight.md`, every file in `tasks/{id}/05_review/`
- Working (this task): the worktree and the PR
- Reference (every task): `_shared/rules.md`, `_shared/history.md`
- Reference (every task): `stages/06_approve/references/gate.md`, `repos/{dir}.md`

Do NOT load: other tasks, the lens files.

## Process
1. Read `history.md` to the end. A `## Feedback from a person` that approves the merge stands in for the gate's judgment items (marked ◆) and item 6, never for the other hard ones.
2. Get the facts: `gh pr view <PR> --json state,isDraft,headRefOid,mergeable,mergeStateStatus,files,additions,deletions,statusCheckRollup` and `git -C <worktree> rev-parse HEAD`.
3. Walk [gate.md](references/gate.md) item by item. Write each as held or failed, with the evidence, in `approval.md`.
4. Route:
   - **Conflicts with the base**: `fail: retry 03 - rebase on {base}: conflicts in <files>`.
   - **Behind the base, no conflicts, and the repo needs it current**: `gh pr update-branch <PR>`, then `fail: retry 04 - branch updated; recheck CI`.
   - **Head moved since preflight or review**: `fail: retry 04 - head changed to <sha>`.
   - **Item 7, 8 or 12 failed for something the builder can do** (a missing test, a browser or simulator check never run, a `should` finding neither fixed nor disputed, a command never run): `fail: retry 03 - <exactly what to prove, run or answer>`. Only proof a person alone can give (a physical device, a real payment, a third-party account) goes to a person.
   - **Every item holds**: `gh pr ready <PR>`, then `gh pr merge <PR> --<merge_method> --match-head-commit <sha> --delete-branch`. Confirm it says `MERGED`. If the issue is still open, close it with a comment naming the merge commit and the base branch. `pass - merged <sha>`.
   - **Any other failed item, or any doubt**: comment on the PR: a three-line summary of the change, each failed item and why, what to look at first, and how to approve (merge on GitHub, or `python3 _tools/factory.py feedback {id} 06_approve "approved"`). Leave it draft. `fail: human - <the failed items>`.
5. Append your handoff, stop.

## A release task
`kind: release` in `TASK.md`: walk the gate's `## Release` items instead of its numbered ones (there is no `05_review`). When every one holds, and the PR isn't already merged, merge it as in step 4 with two differences: always `--merge` (a merge commit), whatever `merge_method` says, because the next release counts what ships from the release branch's ancestry and a squash or rebase loses it (merge commits not allowed in the repo: `fail: human`); and leave the issue open, since it closes only in step 3 below. Releases differ per repo: what follows the merge is the profile's `## Release`, nothing else.
1. **Deploy**: if it names one, follow the run the merge started to the end. Its SHA is the merge commit (`gh pr view <PR> --json mergeCommit -q .mergeCommit.oid`), not the PR head (`gh run list --workflow <deploy> --commit <merge sha>`, then `gh run watch <id> --exit-status`; give up after 30 minutes). Failed or never started: `fail: human - deploy failed on <merge sha>: <run URL>`, saying what production may now be running.
2. **After merge**: do its steps in order, skipping any already done (a retry or a person's feedback resumes here). A step that fails, or one you can't do exactly as written: `fail: human - <step>: <why>`. Merging any PR a step opens (a sync back, say) needs its required checks green first.
3. Only now close the issue, with what shipped and where. `pass - released {version} at <merge sha>`.

## Outputs
- `tasks/{id}/06_approve/approval.md`: the gate, item by item, with evidence; the merge commit or the PR comment you left.
- `tasks/{id}/06_approve/check.md`: `pass - merged <sha>`, `fail: retry NN - <why>` or `fail: human - <why>`.
- A handoff appended to `tasks/{id}/history.md`.

## Check
GitHub is the check on a merge: the PR reads `MERGED` at the SHA the panel saw. Everything else stops with a person, who merges, sends feedback or rejects; the runner notices a merge or close done by hand on its next pull.
