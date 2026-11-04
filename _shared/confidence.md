# Confidence gate - when the factory stops for a person

Every check writes `check.md` beside its stage's output, three lines:

```
pass | fail: retry - <why> | fail: human - <why>
confidence: <0-5>
attempt: <n>   (the attempt number you were given; 1 if none)
```

Confidence scale, used by every check and every review finding: **5** confirmed by a test or reproduction, **4** strong evidence and no credible alternative, **3** probable but unverified, **0–2** a guess.

## Verdicts
- **pass**: confidence 4 or 5, and nothing below in "Always human" applies.
- **fail: retry**: a fixable problem with a clear fix. Go back to the stage the contract names, with this `check.md` and its findings as input. At most 3 retries per stage per task; the runner counts them and turns the next into `fail: human`.
- **fail: human**: confidence 3 or lower, a decision the spec does not contain, retries used up, or an always-human trigger.

## On `fail: human`
1. Add label `factory:needs-human` to the issue or PR and comment the why in one paragraph.
2. The runner (`_tools/factory.py`) sends a macOS notification. Run by hand, report it in chat.
3. Stop that task only. Other tasks keep going.

The person resumes it by fixing or deciding, changing line 1 of `check.md` to `pass - <what they decided>`, removing the label, adding one line to [lessons](lessons.md), then `python3 _tools/factory.py resume {run}`.

## Always human, whatever the confidence
Recommended defaults; a repo profile can add paths, and a person can delete a line here.
- A migration that drops, renames or rewrites existing data.
- Changes to auth, permissions, payments or secrets handling.
- A failed deploy verification (after the automatic rollback).
- The first production deploy of a repo through the factory.
