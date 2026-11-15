# Onboard a repo - give the factory what it needs, once

One job: write `repos/{dir}.md` for a repo folder beside the factory that has no profile yet.

## Inputs
- Working: the repo folder `../{dir}` (if it is not there, clone it there with `gh repo clone {owner}/{name} ../{dir}`)
- Reference: `_templates/repo.md`, `_shared/confidence.md`

## Process
1. Copy `_templates/repo.md` to `repos/{dir}.md`; set `path: ../{dir}` and `repo:` from `git -C ../{dir} remote get-url origin`.
2. Fill it from the repo itself: `package.json` scripts or the build file, `.github/workflows/`, the repo's `AGENTS.md` / `CLAUDE.md`, deploy config (`vercel.json`, `fly.toml`, `wrangler.toml`, a deploy workflow), env files that git ignores but builds need (`git -C ../{dir} ls-files --others --ignored --exclude-standard | grep -E '(^|/)\.env'`), and branch protection via `gh api repos/{owner}/{name}/branches/{default}/protection`.
3. Ask the person only what the repo could not answer: usually verify, rollback, protected paths and always-human paths. Give each question a recommended answer.
4. Create the labels: `gh label create {label} -R {owner}/{name} --force` for `factory:idea`, `factory`, `factory:ready`, `factory:needs-info`, `factory:needs-human`.

## Check
The person reads the profile and approves it. Deploy, verify and rollback are the lines an agent must not guess. This is the one human step per repo.
