# Confidence gate - when the factory stops for a person

Every check writes `check.md` beside its stage's output, three lines:

```
pass | fail: retry - <why> | fail: human - <why> | wait: author - <why> | reject - <why>
confidence: <0-5>
attempt: <n>   (the attempt number you were given; 1 if none)
```

Confidence scale, used by every check and every review finding: **5** confirmed by a test or reproduction, **4** strong evidence and no credible alternative, **3** probable but unverified, **0–2** a guess.

## Verdicts
- **pass**: confidence 4 or 5, and nothing below in "Always human" applies.
- **fail: retry**: a fixable problem with a clear fix. Go back to the stage the contract names, with this `check.md` and its findings as input. At most 3 retries per stage per task; the runner counts them and turns the next into `fail: human`.
- **fail: human**: confidence 3 or lower, a decision the spec does not contain, retries used up, or an always-human trigger.
- **wait: author** and **reject**: only at 01 for an idea that came from an issue; see [01_ideate](../stages/01_ideate/CONTEXT.md). The runner posts the question or the why on the issue. A question labels it `factory:needs-info` and the next `pull` resumes the run once the author replies.

The runner also writes a verdict itself, with no agent: `fail: human` when a stage changed the factory's own files, and `fail: retry - 05` when a PR touches a protected path (`_shared/rules.md`).

## On `fail: human`
1. Add label `factory:needs-human` to the issue or PR and comment the why in one paragraph.
2. The runner (`_tools/factory.py`) sends a macOS notification. Run by hand, report it in chat.
3. Stop that task only. Other tasks keep going.

The person then does one of these, and adds one line to [lessons](lessons.md):
- **Decide it passes**: change line 1 of `check.md` to `pass - <what they decided>`, remove the label, then `python3 _tools/factory.py resume {run}`.
- **Send it back with notes**: `python3 _tools/factory.py feedback {run} [{issue}] "<what to change>"`. A task goes back to 05; a run goes back to the stage that stopped. The notes land in that stage's folder as `feedback-{k}.md` and the retry count starts over.
- **Drop it**: `python3 _tools/factory.py reject {run} [{issue}] "<why>"`. The why goes on the issue, the factory labels come off, and the task's PR closes. The issue stays open.

## Always human, whatever the confidence
Only the two that cannot be undone; a repo profile can add paths.
- A migration that drops, renames or rewrites existing data.
- A failed deploy verification (after the automatic rollback).
