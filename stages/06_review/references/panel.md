# Review panel - who reviews a PR and how they rule

Each seat is a fresh agent that follows [review-code](../../../skills/review-code/SKILL.md) through one lens.

| Seat | Lens | When |
|---|---|---|
| correctness | [correctness](../../../skills/review-code/lenses/correctness.md) | always |
| security | [security](../../../skills/review-code/lenses/security.md) | always |
| performance | [performance](../../../skills/review-code/lenses/performance.md) | always |
| slop | [slop](../../../skills/review-code/lenses/slop.md) | always |
| tests | [tests](../../../skills/review-code/lenses/tests.md) | always |
| accessibility | [accessibility](../../../skills/review-code/lenses/accessibility.md) | the profile says yes and the diff touches UI |

## Aggregation rule
- `fail: human` if any seat says `Blocked`, a Must fix sits at confidence 3, or any finding touches an always-human trigger (`_shared/confidence.md` or the profile).
- `fail: retry - 05` if any Must fix or Should fix sits at confidence 4 or more.
- `pass` otherwise. Could-fix findings are listed in `verdict.md` but do not block.
