# Review panel - who reviews a PR and how they rule

Each seat is a `factory-reviewer` agent, launched on the seat's model, that follows [review-code](../../../skills/review-code/SKILL.md) through one lens. The deepest lenses get the strongest model.

| Seat | Lens | Model | When |
|---|---|---|---|
| correctness | [correctness](../../../skills/review-code/lenses/correctness.md) | opus | always |
| security | [security](../../../skills/review-code/lenses/security.md) | opus | always |
| performance | [performance](../../../skills/review-code/lenses/performance.md) | sonnet | always |
| slop | [slop](../../../skills/review-code/lenses/slop.md) | sonnet | always |
| tests | [tests](../../../skills/review-code/lenses/tests.md) | sonnet | always |
| accessibility | [accessibility](../../../skills/review-code/lenses/accessibility.md) | sonnet | the profile says yes and the diff touches UI |

## Aggregation rule
- `fail: human` if any seat says `Blocked`, a Must fix sits at confidence 3, or any finding touches an always-human trigger (`_shared/confidence.md` or the profile).
- `fail: retry - 05` if any Must fix or Should fix sits at confidence 4 or more.
- `pass` otherwise. Could-fix findings are listed in `verdict.md` but do not block.
