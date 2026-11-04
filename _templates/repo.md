---
repo: {owner}/{name}
path: ../{dir}
default_branch: main
merge_method: squash
---
# {dir} - repo profile

Everything the factory needs to build, merge and ship this repo. `path:` is the repo's folder beside the factory, relative to the factory root. Filled by `setup/onboard-repo.md`.

## Commands
- install: `{e.g. bun install}`
- test: `{e.g. bun test}`
- lint / typecheck: `{...}`
- dev server, for browser proof: `{...}`
- env files: `{paths relative to the repo that git ignores but builds need, e.g. apps/web/.env; or none}`

## CI
- required checks: {from branch protection, or "none"}

## Deploy
- how: {auto on merge to the default branch via <platform> | run `{command}`}
- wait for it: `{command that shows the deployment for a commit, e.g. gh api repos/{owner}/{name}/deployments?sha={sha}}`
- preview url: `{command that prints the preview deploy URL for a PR, e.g. from its deployment status; or none}`
- verify: `{command that exits 0 only when the change is live and healthy}`
- rollback: `{command}` (default if blank: open a PR reverting the merge commit, merge it, deploy, verify)
- first factory deploy done: no

## Review panel
- performance seat: {web | general}
- accessibility seat: {yes | no}

## Always human (adds to `_shared/confidence.md`)
- paths: {e.g. `packages/auth/**`, `**/migrations/**`}
