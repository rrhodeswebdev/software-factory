---
name: new-task
description: Turns a request into one or more well-formed factory tasks (GitHub issues labelled factory) in an onboarded repo. Use when the person says "new task", "add a task", "file this for the factory", or describes work they want the factory to do.
---
# new-task - write a task the factory can finish

A task is a GitHub issue labelled `factory`. The better it says what done looks like, the less triage and spec have to guess.

A release (ship the default branch to production) isn't written by hand: run the [factory](../factory/SKILL.md) skill's `release` row.

1. **Which repo.** Match the person's words to a profile in `repos/`. None fits: offer the [onboard-repo](../onboard-repo/SKILL.md) skill first.
2. **Understand it.** If the ask is unclear about what done looks like, ask one question at a time, each with your recommended answer. Stop asking once you could write the "Done when" lines.
3. **One PR each.** Work bigger than about 400 changed lines, or two concerns at once, becomes several tasks. Order them, and give each later one `Depends on: #n`.
4. **Write each body** from [the issue template](../../_templates/issue.md): Problem, Done when (observable, testable lines), Context, Out of scope, Depends on. Keep it short; don't design the solution.
5. **Show the person** the title and body of every task before filing. File only what they approve.
6. **File each**, in dependency order so the numbers exist:
   `python3 _tools/factory.py new {dir} "{title}" "{body}"`
   It prints the issue URL. Put real issue numbers in later tasks' `Depends on` lines.
7. Tell the person the URLs, and that `python3 _tools/factory.py pull` (or a running `watch`) picks them up.
