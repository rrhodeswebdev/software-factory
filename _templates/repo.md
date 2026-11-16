---
repo: {owner}/{name}
default_branch: main
merge_method: squash
auto_merge: true
release_branch: none
release_head: release/{version}
---
# {dir} - repo profile

Everything the factory's agents need to build, check and merge in this repo. The file name is the repo's folder beside the factory (`../{dir}`). The frontmatter is read by `_tools/factory.py`: `default_branch` is where PRs go, `merge_method` is `squash`, `merge` or `rebase`, and `auto_merge: false` makes the approver always ask a person. `release_branch` is where a release PR goes (production, e.g. `main`); `none` means the factory never releases this repo. `release_head` is the release PR's branch name.

{One paragraph: what the repo is, its stack, and where its own agent guide lives (AGENTS.md, CLAUDE.md, CONTRIBUTING.md). Agents follow that guide inside the repo.}

## Commands
Run from the worktree root. Write `none` when the repo has none; agents never invent one.
- install:
- format / lint (auto-fix):
- lint (check):
- typecheck:
- test:
- build:
- dev server, for UI proof (`{port}` is filled by the agent):

## CI
- required checks: {names, or "none"}

## Protected paths
A PR that touches one always goes to a person. Workflows, env files and secrets are always protected; add the repo's own.
- `.github/workflows/*`
- `.env*`

## Release
Only when `release_branch` isn't `none`. Every repo releases its own way: this section is the whole recipe the release task follows, beside the repo's own release guide.
- version: {how it's numbered, e.g. semver from conventional commits; `factory.py release` picks semver itself only when the tags are `vX.Y.Z`}
- release files: {what the release commit changes, e.g. `package.json` `version`, `CHANGELOG.md`}
- before merge: {checks beyond CI, or `none`}
- deploy: {the workflow a merge into `release_branch` runs, or `none`}
- after merge: {numbered steps: tag, GitHub release, publish, sync back into the default branch; or `none`}

## Notes
{Anything an agent would otherwise get wrong: branch rules, what never to touch, how issues get closed.}
