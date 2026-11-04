#!/usr/bin/env python3
"""Run the software factory: every stage is a fresh, headless Claude Code process.

    python3 _tools/factory.py new <dir> "<idea>"   start a run for ../<dir> and drive it to the end
    python3 _tools/factory.py resume <run>          continue a run from its first stage without a pass
    python3 _tools/factory.py pull [<dir> ...]      build every factory:ready issue (every onboarded repo if none named)
    python3 _tools/factory.py status                one line per run: ✓ pass  ↻ retry  ✋ needs a person  · not run

Standard library only; run from anywhere. Stops a task, labels it and sends a macOS notification
whenever a check says `fail: human`, a stage times out, or retries run out (_shared/confidence.md).
"""
import concurrent.futures as cf
import datetime
import fcntl
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
RUN_STAGES = ["01_ideate", "02_spec", "03_plan", "04_issues"]
TASK_STAGES = ["05_build", "06_review", "07_merge", "08_deploy"]
STAGE_TIMEOUT = 60 * 60   # seconds; a stuck agent stops here and asks for a person
MAX_RUNS_PER_STAGE = 4    # first try + 3 retries
PARALLEL_TASKS = 3
# User-level settings, plugins and MCP servers are left out so only the factory's own skills apply.
# shortcut: "auto" can deny a risky command (merge, deploy) with nobody to ask; if stages stall on that, use "bypassPermissions".
CLAUDE = ["claude", "--permission-mode", "auto", "--permission-prompts", "none",
          "--setting-sources", "project,local", "--strict-mcp-config", "--add-dir", str(ROOT.parent), "-p"]


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def notify(msg):
    print(msg, flush=True)
    subprocess.run(["osascript", "-e", f'display notification {json.dumps(msg)} with title "Software Factory"'],
                   check=False, capture_output=True)


def folder(run, stage, issue=None):
    return (RUNS / run if issue is None else RUNS / run / "tasks" / str(issue)) / stage


def verdict(run, stage, issue=None):
    f = folder(run, stage, issue) / "check.md"
    lines = f.read_text().strip().splitlines() if f.exists() else []
    return lines[0].strip() if lines else ""


def repo_of(run):
    return re.search(r"^repo:\s*(\S+)", (RUNS / run / "RUN.md").read_text(), re.M)[1]


def run_stage(run, stage, issue=None, attempt=1):
    target = f"run `{run}`" + (f", issue #{issue}" if issue else "")
    prompt = (f"Software factory, stage {stage}, {target}, attempt {attempt}. Read AGENTS.md, then "
              f"stages/{stage}/CONTEXT.md, and do exactly that stage: write its outputs and check.md, then stop. "
              "Use only this factory's skills/ and nothing installed elsewhere.")
    out = folder(run, stage, issue)
    out.mkdir(parents=True, exist_ok=True)
    (out / "check.md").unlink(missing_ok=True)  # a stale verdict must never count for this attempt
    try:
        with (out / "agent.log").open("a") as log:
            subprocess.run(CLAUDE + [prompt], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=STAGE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"fail: human - timed out after {STAGE_TIMEOUT // 60} min"
    return verdict(run, stage, issue) or "fail: human - the agent wrote no check.md (see agent.log)"


def stop(run, stage, issue, why):
    if issue:
        subprocess.run(["gh", "issue", "edit", str(issue), "-R", repo_of(run), "--add-label", "factory:needs-human"],
                       check=False, capture_output=True)
    notify(f"Needs you: {run}{f' #{issue}' if issue else ''} {stage}: {why}")
    return why


def drive(run, stages, issue=None, run_stage=run_stage):
    """Run stages from the first without a pass. Return None when all pass, else why it stopped."""
    i = next((n for n, s in enumerate(stages) if not verdict(run, s, issue).startswith("pass")), len(stages))
    tries = {}
    while i < len(stages):
        stage = stages[i]
        tries[stage] = tries.get(stage, 0) + 1
        if tries[stage] > MAX_RUNS_PER_STAGE:
            return stop(run, stage, issue, "fail: human - retries used up")
        v = run_stage(run, stage, issue, tries[stage])
        if v.startswith("pass"):
            i += 1
        elif v.startswith("fail: retry"):
            m = re.search(r"\b(0\d)\b", v)  # "fail: retry - 05 ..." goes back to 05; no number means this stage
            back = next((n for n, s in enumerate(stages) if s[:2] == m[1]), None) if m else i
            if back is None:  # sent outside this list, e.g. a task back to 03: a person decides
                return stop(run, stage, issue, v)
            i = back
        else:
            return stop(run, stage, issue, v)
    return None


def lock(path):
    f = open(path, "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return f
    except BlockingIOError:
        return None


def deps(repo, issue):
    body = gh("issue", "view", str(issue), "-R", repo, "--json", "body", "-q", ".body")
    sec = re.search(r"## Depends on\n(.*?)(?:\n## |\n---|\Z)", body, re.S)
    return [int(n) for n in re.findall(r"#(\d+)", sec[1])] if sec else []


def closed(repo, issue):
    return gh("issue", "view", str(issue), "-R", repo, "--json", "state", "-q", ".state").strip() == "CLOSED"


def run_tasks(run, issues):
    repo = repo_of(run)
    waiting = {n: deps(repo, n) for n in issues}

    def ready(n):
        return all(verdict(run, "07_merge", d).startswith("pass") or closed(repo, d) for d in waiting[n])

    # shortcut: tasks run in waves (a wave waits for its slowest task); pipeline them if waves get long.
    with cf.ThreadPoolExecutor(PARALLEL_TASKS) as pool:
        while batch := [n for n in waiting if ready(n)]:
            for n in batch:
                del waiting[n]
            list(pool.map(lambda n: drive(run, TASK_STAGES, n), batch))
    for n, on in waiting.items():
        print(f"{run} #{n} still waits on {on}")


def is_pull_run(run):
    return re.search(r"-issue-\d+$", run) is not None


def task_issues(run):
    f = folder(run, "04_issues") / "issues.md"
    if f.exists():
        return [int(n) for n in re.findall(r"^\|\s*T\d+\s*\|\s*#?(\d+)\s*\|", f.read_text(), re.M)]
    t = RUNS / run / "tasks"
    return sorted(int(p.name) for p in t.iterdir() if p.name.isdigit()) if t.exists() else []


def resume(run):
    held = lock(RUNS / run / ".lock")
    if not held:
        sys.exit(f"{run} is already being driven by another factory process")
    if is_pull_run(run) or drive(run, RUN_STAGES) is None:
        run_tasks(run, task_issues(run))
    status([run])


def start_run(dir_, run, idea):
    profile = ROOT / "repos" / f"{dir_}.md"
    if not profile.exists():
        sys.exit(f"no profile for ../{dir_}: onboard it first (setup/onboard-repo.md)")
    repo = re.search(r"^repo:\s*(\S+)", profile.read_text(), re.M)[1]
    (RUNS / run).mkdir(parents=True, exist_ok=False)
    fill = {"{owner}/{name}": repo, "{dir}": dir_, "{YYYY-MM-DD}": str(datetime.date.today()),
            "{run-id}": run, "{the idea, as the person gave it}": idea}
    text = (ROOT / "_templates" / "run.md").read_text()
    for k, v in fill.items():
        text = text.replace(k, v)
    (RUNS / run / "RUN.md").write_text(text)


def new(dir_, idea):
    slug = re.sub(r"[^a-z0-9]+", "-", idea.lower()).strip("-")[:40].strip("-")
    run = f"{datetime.date.today()}-{dir_}-{slug}"
    start_run(dir_, run, idea)
    resume(run)


def pull(dirs):
    if not lock(ROOT / ".factory.lock"):
        sys.exit("another pull is running")
    for dir_ in dirs or sorted(p.stem for p in (ROOT / "repos").glob("*.md") if p.stem != "CONTEXT"):
        repo = re.search(r"^repo:\s*(\S+)", (ROOT / "repos" / f"{dir_}.md").read_text(), re.M)[1]
        by_run = {}
        for it in json.loads(gh("issue", "list", "-R", repo, "--label", "factory:ready",
                                "--json", "number,body", "--limit", "100")):
            m = re.search(r"Factory run: `([^`]+)`", it["body"])
            run = m[1] if m and (RUNS / m[1]).exists() else f"{datetime.date.today()}-{dir_}-issue-{it['number']}"
            if not (RUNS / run).exists():
                start_run(dir_, run, f"Pulled issue #{it['number']}")
            by_run.setdefault(run, []).append(it["number"])
        for run, issues in by_run.items():
            held = lock(RUNS / run / ".lock")
            if held:  # a run another process is driving is left to it
                run_tasks(run, issues)


MARK = {"pass": "✓", "fail: retry": "↻", "fail: human": "✋"}


def mark(v):
    return next((m for k, m in MARK.items() if v.startswith(k)), "·")


def status(runs=None):
    for run in runs or sorted(p.name for p in RUNS.iterdir() if p.is_dir()):
        parts = [] if is_pull_run(run) else [" ".join(s[:2] + mark(verdict(run, s)) for s in RUN_STAGES)]
        for n in task_issues(run):
            parts.append(f"#{n} " + " ".join(s[:2] + mark(verdict(run, s, n)) for s in TASK_STAGES))
        print(f"{run}  {' | '.join(parts)}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["status"]
    commands = {"new": lambda: new(args[0], " ".join(args[1:])), "resume": lambda: resume(args[0]),
                "pull": lambda: pull(args), "status": lambda: status()}
    if cmd not in commands or (cmd in ("new", "resume") and not args):
        sys.exit(__doc__)
    commands[cmd]()
