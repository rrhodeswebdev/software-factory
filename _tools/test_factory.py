"""Self-check for the runner's retry and stop logic. Run: python3 -I _tools/test_factory.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import factory  # noqa: E402

factory.RUNS = Path(tempfile.mkdtemp())
factory.notify = lambda msg: None
STAGES = factory.TASK_STAGES


def fake(script):
    """A run_stage that writes the next scripted verdict for each stage and records the calls."""
    calls = []

    def run_stage(run, stage, issue, attempt):
        v = script[stage].pop(0)
        out = factory.folder(run, stage, issue)
        out.mkdir(parents=True, exist_ok=True)
        (out / "check.md").write_text(v + "\n")
        calls.append(stage[:2])
        return v
    return run_stage, calls


# review sends the build back once, then everything passes
rs, calls = fake({"05_build": ["pass", "pass"], "06_review": ["fail: retry - 05 slop", "pass"],
                  "07_merge": ["pass"], "08_deploy": ["pass"]})
assert factory.drive("r1", STAGES, 1, rs) is None
assert calls == ["05", "06", "05", "06", "07", "08"], calls

# a human verdict stops the task where it is
rs, calls = fake({"05_build": ["pass"], "06_review": ["fail: human - Blocked"]})
assert factory.drive("r2", STAGES, None, rs) == "fail: human - Blocked"
assert calls == ["05", "06"], calls

# resuming skips stages that already pass (the person wrote pass into 06)
(factory.folder("r2", "06_review") / "check.md").write_text("pass - decided by person\n")
rs, calls = fake({"07_merge": ["pass"], "08_deploy": ["pass"]})
assert factory.drive("r2", STAGES, None, rs) is None
assert calls == ["07", "08"], calls

# endless retries are capped
rs, calls = fake({"05_build": ["pass"] * 9, "06_review": ["fail: retry - 05"] * 9})
assert factory.drive("r3", STAGES, None, rs) == "fail: human - retries used up"

# a task sent back to a stage outside its list stops for a person
rs, calls = fake({"05_build": ["fail: retry - 03 issue lacks a decision"]})
assert factory.drive("r4", STAGES, None, rs).startswith("fail: retry - 03")

print("ok")
