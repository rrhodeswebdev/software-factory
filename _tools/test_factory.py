"""Tests for the runner's routing and the dashboard's reading of disk. Run: python3 -m unittest _tools/test_factory.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard as D  # noqa: E402
import factory as F  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = Path(self.tmp.name) / "site-7"
        self.t.mkdir()
        (self.t / "TASK.md").write_text("---\nrepo: me/site\ndir: site\nissue: 7\ntitle: A: b\nurl: u\n"
                                        "branch: factory/7-a\nbase: main\n---\n# site-7\n")
        (self.t / "history.md").write_text("# History\n")
        for name in ("try_gh", "notify", "remove_worktree"):
            p = mock.patch.object(F, name)
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def check(self, stage, text):
        (self.t / stage).mkdir(exist_ok=True)
        (self.t / stage / "check.md").write_text(text + "\n")


class StateTest(Base):
    def test_first_stage_without_pass_is_next(self):
        self.check("01_triage", "pass")
        self.assertEqual(F.state(self.t), ("todo", "02_spec", ""))

    def test_human_stop_and_done_and_rejected(self):
        self.check("01_triage", "fail: human - unclear")
        self.assertEqual(F.state(self.t)[0], "human")
        self.check("06_approve", "pass - merged abc")  # a person merged it: done whatever came before
        self.assertEqual(F.state(self.t)[0], "done")
        (self.t / "rejected.md").write_text("nope\n")
        self.assertEqual(F.state(self.t)[0], "rejected")

    def test_meta_keeps_colons_in_title(self):
        self.assertEqual(F.meta(self.t)["title"], "A: b")


class DriveTest(Base):
    def fake(self, script):
        """A run_stage that returns the next scripted verdict for each stage and writes it like an agent."""
        calls = []

        def run(t, s, attempt):
            calls.append(s)
            v = script[s].pop(0)
            self.check(s, v)
            return v
        return run, calls

    def test_all_pass_finishes(self):
        run, calls = self.fake({s: ["pass"] for s in F.STAGES})
        self.assertEqual(F.drive(self.t, run), "done")
        self.assertEqual(calls, F.STAGES)

    def test_review_retry_reruns_build_and_preflight(self):
        script = {s: ["pass"] for s in F.STAGES}
        script["03_build"] = ["pass", "pass"]
        script["04_preflight"] = ["pass", "pass"]
        script["05_review"] = ["fail: retry 03 - blocking findings from security", "pass"]
        run, calls = self.fake(script)
        self.assertEqual(F.drive(self.t, run), "done")
        self.assertEqual(calls, ["01_triage", "02_spec", "03_build", "04_preflight", "05_review",
                                 "03_build", "04_preflight", "05_review", "06_approve"])

    def test_retry_clears_later_checks_so_a_restart_resumes_at_the_target(self):
        for s in F.STAGES[:4]:
            self.check(s, "pass")

        def run(t, s, attempt):
            raise KeyboardInterrupt  # the process dies right after routing back
        script = {"05_review": ["fail: retry 03 - x"]}
        first, _ = self.fake(script)
        with self.assertRaises(KeyboardInterrupt):
            F.drive(self.t, lambda t, s, a: first(t, s, a) if s == "05_review" else run(t, s, a))
        self.assertEqual(F.state(self.t)[1], "03_build")

    def test_retries_run_out_and_stop_for_a_person(self):
        run, calls = self.fake({"01_triage": ["fail: retry - flaky"] * 5})
        v = F.drive(self.t, run)
        self.assertTrue(v.startswith("fail: human - 01_triage ran 3 times"))
        self.assertEqual(len(calls), 3)
        self.assertEqual(F.state(self.t)[0], "human")

    def test_triage_reject(self):
        run, _ = self.fake({"01_triage": ["reject - already done at a.py:3"]})
        self.assertEqual(F.drive(self.t, run), "reject - already done at a.py:3")
        self.assertEqual(F.state(self.t)[0], "rejected")

    def test_unknown_verdict_stops(self):
        run, _ = self.fake({"01_triage": ["looks good"]})
        self.assertTrue(F.drive(self.t, run).startswith("fail: human - unreadable verdict"))

    def test_back_to_never_goes_forward(self):
        self.assertEqual(F.back_to("fail: retry 03 - x", 4), 2)
        self.assertEqual(F.back_to("fail: retry 06 - x", 2), 2)
        self.assertEqual(F.back_to("fail: retry - x", 3), 3)


class ReleaseTest(Base):
    def make_release(self):
        t = self.t.parent / "site-8"
        F.create(t, "site", {"repo": "me/site", "base": "develop", "release": "main", "head": "release/{version}"},
                 {"number": 8, "title": "Release 1.2.0", "url": "u", "labels": [{"name": F.RELEASE}]})
        return t

    def test_issue_becomes_release_card(self):
        m = F.meta(self.make_release())
        self.assertEqual((m["kind"], m["base"], m["branch"]), ("release", "main", "release/1.2.0"))
        self.assertEqual(F.meta(self.t)["kind"], None)
        t = self.t.parent / "site-9"
        F.create(t, "site", {"repo": "me/site", "base": "main", "release": "main", "head": "rel-{version}"},
                 {"number": 9, "title": "Release v2026.11", "url": "u", "labels": [{"name": F.RELEASE}]})
        self.assertEqual(F.meta(t)["branch"], "rel-2026.11")  # each repo names and numbers its own  # cards from before releases stay ordinary tasks

    def test_release_runs_only_build_preflight_approve(self):
        t = self.make_release()
        self.assertEqual(F.state(t), ("todo", "03_build", ""))
        calls = []

        def run(t_, s, attempt):
            calls.append(s)
            v = "fail: retry 03 - bump" if s == "04_preflight" and calls.count(s) == 1 else "pass"
            (t_ / s).mkdir(exist_ok=True)
            (t_ / s / "check.md").write_text(v + "\n")
            return v
        self.assertEqual(F.drive(t, run), "done")
        self.assertEqual(calls, ["03_build", "04_preflight", "03_build", "04_preflight", "06_approve"])

    def test_merged_release_pr_waits_for_a_person(self):
        t = self.make_release()
        (t / "03_build").mkdir()
        (t / "03_build" / "build.md").write_text("PR: https://github.com/me/site/pull/9\n")
        with mock.patch.object(F, "gh", return_value='{"state": "MERGED"}'), mock.patch.object(F, "finish") as fin:
            F.reconcile(t)
            fin.assert_not_called()
        self.assertFalse((t / "06_approve" / "check.md").exists())

    def test_next_version(self):
        self.assertEqual(F.next_version("v0.7.0", ["fix: a", "chore(deps): b"]), "0.7.1")
        self.assertEqual(F.next_version("v0.7.3", ["fix: a", "feat(404): b"]), "0.8.0")
        self.assertEqual(F.next_version("0.7.3", ["feat!: drop x", "feat: y"]), "1.0.0")
        with self.assertRaises(ValueError):  # calver and the like: the person names the version
            F.next_version("2026.11", ["feat: a"])


class ParseTest(Base):
    def test_deps(self):
        self.assertEqual(F.deps("Fix it.\n\nDepends on: #12, #14 and #3"), ["12", "14", "3"])
        self.assertEqual(F.deps("No deps; see #9"), [])

    def test_panel_always_has_code_and_drops_unknown_lenses(self):
        p = Path(self.tmp.name) / "panel.md"
        p.write_text("- security: login form\n- `ui-ux`: new page\n- astrology: no\n- security: twice\n")
        self.assertEqual(F.read_panel(p), ["code", "security", "ui-ux"])
        p.write_text("nothing useful")
        self.assertEqual(F.read_panel(p), F.DEFAULT_PANEL)

    def test_every_lens_names_a_model_and_when(self):
        for f in F.LENSES.glob("*.md"):
            self.assertTrue(F.field(f.read_text(), "model"), f.name)
            self.assertTrue(F.field(f.read_text(), "use when"), f.name)


class DashboardTest(Base):
    def test_doing_reads_last_tool_call(self):
        log = Path(self.tmp.name) / "agent.log"
        log.write_text("\n".join(json.dumps(e) for e in [
            {"type": "system"},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "Reading the spec"}]}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash",
                                                           "input": {"command": "bun run build"}}]}},
            {"type": "user", "message": {"content": []}}]) + "\nnot json\n")
        self.assertEqual(D.doing(log), "Bash: bun run build")

    def test_task_info_marks_live_agents_running(self):
        self.check("01_triage", "pass")
        (self.t / "02_spec").mkdir()
        (self.t / "02_spec" / "running.json").write_text(json.dumps(
            {"agent": "factory-spec", "pid": __import__("os").getpid(), "started": 0, "log": "agent.log"}))
        info = D.task_info(self.t)
        self.assertEqual((info["state"], info["agents"][0]["stage"]), ("running", "02_spec"))


if __name__ == "__main__":
    unittest.main()
