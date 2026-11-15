# 01_ideate - raw idea to decided brief

One job: turn a raw idea into a brief a designer can spec without asking anything.

## Inputs
- Working (this run): `runs/{run}/RUN.md` (repo, profile link, and the idea under `## Idea`), or the idea in chat
- Working (after the author answers): `runs/{run}/01_ideate/replies.md`, the author's replies, quoted by the runner
- Reference (every run): `skills/refine-idea/SKILL.md`
- Reference (every run): the repo profile that `runs/{run}/RUN.md` links to, plus the target repo's `README` and `AGENTS.md` / `CLAUDE.md` at the profile's `path:`
- Reference (every run): `_shared/confidence.md`

Do NOT load: other runs, the repo's source beyond what grounds the idea, later stages' contracts.

## Process
1. If the repo has no profile in `repos/`, stop: onboard it first (`setup/onboard-repo.md`).
2. Follow `refine-idea`.

## Outputs
- `runs/{run}/01_ideate/idea.md`
- `runs/{run}/01_ideate/questions.md`, only when the check is `wait: author`: the questions the runner posts on the issue

## Check
An issue run (`source: #n` in `RUN.md`) has two more verdicts, used only here (`_shared/confidence.md`):
- `reject - <why>` when, at confidence 4 or more, this should not be built: it is outside what the repo is for, harmful or abusive, already done, or a duplicate. The runner posts the why on the issue.
- `wait: author - <one line>` when a question only the issue's author can answer would change what gets built. Write `questions.md` first: each question with your recommended answer, short enough to read on GitHub.

If the person is in the conversation, their go-ahead is the pass: write `pass`, confidence 5. Otherwise a `factory-checker` agent reads `idea.md` and answers: could a designer spec this without a question that changes behavior? It writes `check.md` per `_shared/confidence.md`. On `fail: retry`, rerun 01.
