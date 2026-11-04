# 08_deploy - merged to live, issue closed

One job: get the merge commit live, prove it is healthy, then close the issue.

## Inputs
- Working (this run): `runs/{run}/tasks/{issue}/07_merge/merge.md` (merge SHA)
- Reference (every run): the repo profile `runs/{run}/RUN.md` links to (its Deploy section), `_shared/rules.md`, `_shared/confidence.md`

Do NOT load: review files, the build, the spec, other tasks.

## Process
1. If `07_merge/check.md` is not `pass`, stop and say so.
2. Deploy the merge SHA the profile's way: wait for the automatic deploy, or run the profile's deploy command.
3. Run the profile's verify command against the deployed SHA.
4. Verified: `gh issue close {issue} -R {repo} --comment "Deployed in {sha}: {url}"`.
5. Not verified: run the profile's rollback, verify the rollback, then `fail: human`. Never retry a failed deploy on your own.

## Outputs
- `runs/{run}/tasks/{issue}/08_deploy/deploy.md`: SHA, deploy URL or log, verify output, issue state

## Check
The verify command exits 0 and `gh issue view {issue} -R {repo} --json state` shows `CLOSED`. Write `check.md` per `_shared/confidence.md`. When every task in the run passes here, the run is done.
