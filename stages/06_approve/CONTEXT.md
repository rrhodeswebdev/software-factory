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
1. Read `history.md` to the end. A `## Feedback from a person` that approves the merge stands in for the gate's judgment items (marked ◆), never for the hard ones.
2. Get the facts: `gh pr view <PR> --json state,isDraft,headRefOid,mergeable,mergeStateStatus,files,additions,deletions,statusCheckRollup` and `git -C <worktree> rev-parse HEAD`.
3. Walk [gate.md](references/gate.md) item by item. Write each as held or failed, with the evidence, in `approval.md`.
4. Route:
   - **Conflicts with the base**: `fail: retry 03 - rebase on {base}: conflicts in <files>`.
   - **Behind the base, no conflicts, and the repo needs it current**: `gh pr update-branch <PR>`, then `fail: retry 04 - branch updated; recheck CI`.
   - **Head moved since preflight or review**: `fail: retry 04 - head changed to <sha>`.
   - **Every item holds**: `gh pr ready <PR>`, then `gh pr merge <PR> --<merge_method> --match-head-commit <sha> --delete-branch`. Confirm it says `MERGED`. If the issue is still open, close it with a comment naming the merge commit and the base branch. `pass - merged <sha>`.
   - **Any other failed item, or any doubt**: comment on the PR: a three-line summary of the change, each failed item and why, what to look at first, and how to approve (merge on GitHub, or `python3 _tools/factory.py feedback {id} 06_approve "approved"`). Leave it draft. `fail: human - <the failed items>`.
5. Append your handoff, stop.

## Outputs
- `tasks/{id}/06_approve/approval.md`: the gate, item by item, with evidence; the merge commit or the PR comment you left.
- `tasks/{id}/06_approve/check.md`: `pass - merged <sha>`, `fail: retry NN - <why>` or `fail: human - <why>`.
- A handoff appended to `tasks/{id}/history.md`.

## Check
GitHub is the check on a merge: the PR reads `MERGED` at the SHA the panel saw. Everything else stops with a person, who merges, sends feedback or rejects; the runner notices a merge or close done by hand on its next pull.
