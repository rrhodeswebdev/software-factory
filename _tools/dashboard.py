#!/usr/bin/env python3
"""The factory dashboard: what every agent is doing, what needs you, and a form to file a task.

    python3 _tools/dashboard.py [<port>]     then open http://127.0.0.1:8787 (default port)

Reads tasks/ from disk on every request, so it never disagrees with `factory.py status`. Listens on
127.0.0.1 only. Standard library only.
"""
import http.server
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import factory as F  # noqa: E402

PAGE = Path(__file__).with_name("dashboard.html")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def tail(path, size=65536):
    try:
        with path.open("rb") as f:
            f.seek(max(0, f.seek(0, 2) - size))
            return f.read().decode("utf-8", "replace")
    except OSError:
        return ""


def doing(log):
    """The agent's latest move, from its stream-json log: the last tool call or the last thing it said."""
    for line in reversed(tail(log).splitlines()):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") != "assistant":
            continue
        for c in reversed(e.get("message", {}).get("content", [])):
            if c.get("type") == "tool_use":
                arg = next((str(c["input"][k]) for k in ("command", "file_path", "pattern", "description", "url")
                            if k in c.get("input", {})), "")
                return f"{c['name']}: {arg}".strip(": ")[:160]
            if c.get("type") == "text" and c.get("text", "").strip():
                return c["text"].strip().splitlines()[0][:160]
    return "starting"


def task_info(t):
    m = F.meta(t)
    st, stage, v = F.state(t)
    agents = []
    for f in sorted(t.glob("*/running*.json")):
        try:
            r = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        if alive(r["pid"]):
            agents.append({"agent": r["agent"], "lens": r.get("lens"), "stage": f.parent.name,
                           "task": t.name, "started": r["started"], "doing": doing(f.parent / r["log"])})
    if agents and st == "todo":
        st = "running"
    hist = t / "history.md"
    events = [ln[2:] for ln in hist.read_text().splitlines() if ln.startswith("- ")] if hist.exists() else []
    return {"id": t.name, "repo": m["repo"], "issue": m["issue"], "title": m["title"], "url": m["url"],
            "pr": F.pr_of(t), "state": st, "stage": stage, "verdict": v,
            "stages": [{"name": s, "verdict": F.verdict(t, s)} for s in F.stages(t)],
            "agents": agents, "last": events[-1] if events else "",
            "updated": hist.stat().st_mtime if hist.exists() else 0}


def runner():
    f = F.LOCKS / "runner.json"
    try:
        r = json.loads(f.read_text())
    except (OSError, ValueError):
        return None
    return {**r, "alive": alive(r["pid"])}


def snapshot():
    tasks = sorted((task_info(t) for t in F.all_tasks()), key=lambda x: -x["updated"])
    return {"now": time.time(), "tasks": tasks, "repos": F.all_dirs(), "runner": runner(),
            "stages": F.STAGES, "max_agents": F.MAX_AGENTS}


def detail(task_id):
    t = F.TASKS / task_id
    if not re.fullmatch(r"[\w.-]+", task_id) or not (t / "TASK.md").exists():
        return None
    files = {}
    for name in ["history.md", *(f"{s}/check.md" for s in F.stages(t))]:
        if (t / name).exists():
            files[name] = (t / name).read_text()
    return {"id": task_id, "files": files}


class Handler(http.server.BaseHTTPRequestHandler):
    def send(self, code, body, kind="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def local(self):
        """Only this machine's browser: blocks DNS rebinding (Host) and cross-site form posts (Origin)."""
        port = self.server.server_address[1]
        hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        origin = self.headers.get("Origin")
        return self.headers.get("Host") in hosts and (origin is None or origin.split("//")[-1] in hosts)

    def do_GET(self):
        if not self.local():
            return self.send(403, {"error": "local only"})
        if self.path == "/":
            return self.send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/state":
            return self.send(200, snapshot())
        if self.path.startswith("/api/task/"):
            d = detail(self.path.removeprefix("/api/task/"))
            return self.send(200, d) if d else self.send(404, {"error": "no such task"})
        self.send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/tasks":
            return self.send(404, {"error": "not found"})
        if not self.local() or self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.send(403, {"error": "local JSON only"})
        try:
            body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 100_000)))
            if not isinstance(body, dict):
                raise ValueError("send a JSON object")
            url = F.new(str(body.get("dir", "")), str(body.get("title", ""))[:200], str(body.get("body", "")))
        except ValueError as e:
            return self.send(400, {"error": str(e)})
        except F.subprocess.CalledProcessError as e:
            return self.send(502, {"error": (e.stderr or "gh failed").strip()})
        self.send(200, {"url": url})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    print(f"Factory dashboard on http://127.0.0.1:{port}", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
