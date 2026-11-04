---
name: build-task
description: Software factory stage 05. Turns one GitHub issue into one pull request with the smallest complete change, proof for every criterion, and green CI.
---
# build-task - one issue to one PR

Run every command from the factory root. `{path}` is the profile's `path:` (a sibling folder such as `../cheergenics`); `{wt}` is `.worktrees/{dir}-{issue}`.

## Steps
1. Read the issue, the target repo's `AGENTS.md` / `CLAUDE.md` / `README`, the profile, and the code the issue touches. Find the helpers and patterns already there before writing anything.
2. Open a worktree on a fresh branch:
   `git -C {path} fetch origin` then `git -C {path} worktree add "$PWD/{wt}" -b factory/{issue}-{slug} origin/{default_branch}`, then link in each of the profile's env files: `git -C {wt} check-ignore -q {file}` must succeed (else stop with `fail: human`: the file could be committed), then `ln -s "$(cd {path} && pwd)/{file}" {wt}/{file}`. Then run the profile's install command inside `{wt}`.
3. Write the change:
   - the smallest change that fully meets the criteria; nothing the issue did not ask for
   - reuse, in order: code already in the repo, the standard library, an installed dependency; add a dependency only if the issue's decisions name it
   - update every caller, test, fixture and config the change touches
   - keep validation at trust boundaries and error handling that prevents data loss
   - comment only the why the code cannot show
4. Prove it with [prove-task](../prove-task/SKILL.md).
5. Read your own diff (`git -C {wt} diff origin/{default_branch}...HEAD`) and remove debug output, commented-out code, unrelated edits and stray TODOs.
6. Commit in the repo's convention (else `feat: {title} (#{issue})`), push, and open the PR:
   `gh pr create -R {repo} --head factory/{issue}-{slug} --base {default_branch} --title "{title}" --body-file {pr body from _templates/pr.md} --label factory`
7. Wait for CI: `gh pr checks {pr} -R {repo} --watch`. Fix failures your change caused. A failure that was already on the default branch is not yours to fix: report it.
8. On a retry, fix each Must fix and Should fix in `verdict.md` on the same branch, prove again, push, and wait for CI again.
9. On a retry for a merge conflict: `git -C {wt} fetch origin && git -C {wt} merge origin/{default_branch}`, resolve keeping the intent of both sides, prove again, push. Merge, never rebase: no force-push.

Never weaken a test, skip a hook, or touch the default branch. Full list: `_shared/rules.md`.
