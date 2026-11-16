---
name: onboard-repo
description: Adds a repo to the software factory by writing its profile in repos/ from the repo itself. Use when the person wants the factory to work in a new repo, says "onboard", or a task names a repo with no profile.
---
# onboard-repo - write a repo's profile

The factory works on repos that live beside it: `../{dir}` from the factory root. Each needs `repos/{dir}.md`.

1. **Find it.** Confirm `../{dir}` exists and is a git repo with a GitHub remote: `git -C ../{dir} remote get-url origin`. Not cloned yet: ask the person to clone it beside the factory.
2. **Read, don't guess.** From the repo: its `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md`, `package.json` scripts or `Makefile` / `pyproject.toml` / `Cargo.toml`, the CI workflows in `.github/workflows/`, and `gh repo view {owner}/{name} --json defaultBranchRef,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`. Check branch protection for required checks if you can: `gh api repos/{owner}/{name}/branches/{branch}/protection`.
3. **Fill the profile.** Copy [the repo template](../../_templates/repo.md) to `repos/{dir}.md` and fill every field. A command the repo lacks is `none`, never invented. `default_branch` is the branch PRs should target; `merge_method` must be one the repo allows. Add protected paths the repo needs (migrations, infra, release config). Under Notes put what an agent would get wrong: branch rules, never-touch areas, how issues get closed.
4. **Prove the commands.** Run install, lint, typecheck, test and build once in the repo (or a throwaway worktree) and note any that fail on the base branch: the factory will stop on those.
5. **Show the person** the profile and ask about `auto_merge`: `true` lets the approver merge when the gate holds; `false` always asks them. They approve before you're done.
6. The factory creates its labels in the repo on the first `pull` or `new`. Point them at the [new-task](../new-task/SKILL.md) skill.

This skill writes into `repos/`, which stage agents may never edit. Run it only in a session with the person, never from a stage.
