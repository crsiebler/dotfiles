"""Isolated runner integration tests; no real harness or personal Git settings."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
import runpy
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "bin/ralph"

FAKE = '''#!/usr/bin/env python3
import json, os, pathlib, subprocess, time
p = pathlib.Path
action = os.environ.get("ACTION", "complete")
with p(os.environ["LOG"]).open("a") as f:
    f.write(json.dumps(dict(argv=__import__('sys').argv, env={k:v for k,v in os.environ.items() if k.startswith('RALPH_')}))+"\\n")
out = dict(version=1, iteration_id=os.environ["RALPH_ITERATION_ID"], story_id=os.environ["RALPH_STORY_ID"], status="completed")
if action == "sleep":
    child = subprocess.Popen([__import__('sys').executable, "-c", "import time; time.sleep(60)"])
    p(os.environ["CHILD"]).write_text(str(child.pid))
    time.sleep(60)
if action == "fail": raise SystemExit(23)
if action == "missing": raise SystemExit(0)
if action == "malformed":
    p(os.environ["RALPH_OUTCOME_FILE"]).write_text("{")
    raise SystemExit(0)
if action == "duplicate-secret":
    p(os.environ["RALPH_OUTCOME_FILE"]).write_text('{"FAKE_SECRET_SENTINEL":1,"FAKE_SECRET_SENTINEL":2}')
    raise SystemExit(0)
if action == "stop": p(".ralph-stop").touch()
if action in ("retry", "repeat", "no-progress", "vary", "staged"):
    if action != "no-progress": p("work").write_text(p("work").read_text()+"x" if p("work").exists() else "x")
    out.update(status="retryable", finding_ids=["F1"], attempted_action="try fix", next_action="try again", evidence="test failure")
    if action == "vary": out["next_action"] += p("work").read_text()
    if action == "staged": subprocess.run(["git", "add", "work"], check=True)
elif action == "blocked": out.update(status="blocked", reason="human approval required")
else:
    plan = json.loads(p("plan.json").read_text())
    for s in plan["userStories"]:
        if s["id"] == out["story_id"] or action == "other-story": s["passes"] = True
    p("plan.json").write_text(json.dumps(plan))
    if action not in ("false-complete", "stop"):
        subprocess.run(["git", "add", "plan.json", "work" ] if p("work").exists() else ["git", "add", "plan.json"], check=True)
        subprocess.run(["git", "commit", "-qm", "story"], check=True)
if action == "stale": out["iteration_id"] = "old"
if action == "wrong-story": out["story_id"] = "S-other"
if action == "dirty-complete": p("uncommitted").write_text("candidate")
p(os.environ["RALPH_OUTCOME_FILE"]).write_text(json.dumps(out))
if action in ("track-outcome", "commit-outcome", "commit-remove-outcome"):
    subprocess.run(["git", "add", os.environ["RALPH_OUTCOME_FILE"]], check=True)
    if action != "track-outcome":
        subprocess.run(["git", "commit", "-qm", "bad artifact"], check=True)
    if action == "commit-remove-outcome":
        subprocess.run(["git", "rm", "--cached", os.environ["RALPH_OUTCOME_FILE"]], check=True)
        subprocess.run(["git", "commit", "-qm", "remove artifact"], check=True)
'''


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1",
                        HOME=str(self.root), XDG_CONFIG_HOME=str(self.root / "config"),
                        LOG=str(self.root / "log"), CHILD=str(self.root / "child"))
        agent = self.root / "config/opencode/agents/ralph.md"
        agent.parent.mkdir(parents=True)
        agent.write_text("fixture")
        binary = self.root / "opencode"
        binary.write_text(FAKE)
        binary.chmod(0o755)
        self.env["PATH"] = str(self.root) + os.pathsep + os.environ["PATH"]
        self.git("init", "-q", "-b", "ralph/test")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.plan: dict[str, Any] = dict(branchName="ralph/test", userStories=[dict(
            id="S1", title="Test", description="Test", acceptanceCriteria=["checks"],
            priority=1, passes=False)])
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "fixture")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, env=self.env, stderr=subprocess.STDOUT).decode().strip()

    def write_plan(self):
        (self.repo / "plan.json").write_text(json.dumps(self.plan))

    def run_cli(self, *args, action="complete"):
        return subprocess.run([sys.executable, str(RUNNER), *args], cwd=self.repo,
                              env=dict(self.env, ACTION=action), text=True, capture_output=True, timeout=15)

    def state(self):
        path = self.repo / self.git("rev-parse", "--git-path", "ralph/state.json")
        return json.loads(path.read_text())

    def add_second_story(self):
        self.plan["userStories"].append(dict(self.plan["userStories"][0], id="S2"))
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "second story")

    def assert_provisional_resume_refused(self):
        self.assertNotEqual(self.run_cli(action="false-complete").returncode, 0)
        before = (self.repo / "plan.json").read_bytes()
        index = (self.repo / ".git/index").read_bytes()
        calls = (self.root / "log").read_bytes()
        result = self.run_cli("--resume")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("committed", result.stderr)
        self.assertEqual((self.root / "log").read_bytes(), calls)
        self.assertEqual((self.repo / "plan.json").read_bytes(), before)
        self.assertEqual((self.repo / ".git/index").read_bytes(), index)

    def test_provisional_single_story_resume_refused(self):
        self.assert_provisional_resume_refused()

    def test_provisional_multi_story_resume_refused(self):
        self.add_second_story()
        self.assert_provisional_resume_refused()

    def test_resume_accepts_reconciled_descendant_delivery(self):
        self.run_cli(action="false-complete")
        self.git("add", "plan.json")
        self.git("commit", "-qm", "human reconciled delivery")
        calls = (self.root / "log").read_bytes()
        result = self.run_cli("--resume")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "log").read_bytes(), calls)
        self.assertEqual(self.state()["status"], "completed")

    def test_resume_refuses_unrelated_delivery_head(self):
        self.run_cli(action="false-complete")
        self.git("add", "plan.json")
        self.git("commit", "-qm", "candidate delivery")
        orphan = self.git("commit-tree", "HEAD^{tree}", "-m", "unrelated fixture history")
        self.git("update-ref", "refs/heads/ralph/test", orphan)
        result = self.run_cli("--resume")
        self.assertIn("descendant", result.stderr)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_resume_preserves_nonfinal_delivery_ancestry(self):
        self.add_second_story()
        result = self.run_cli("--max-iterations", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()["status"], "ready")
        orphan = self.git("commit-tree", "HEAD^{tree}", "-m", "unrelated history")
        self.git("update-ref", "refs/heads/ralph/test", orphan)
        calls = (self.root / "log").read_bytes()
        result = self.run_cli("--resume")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("descendant", result.stderr)
        self.assertEqual((self.root / "log").read_bytes(), calls)

    def test_completed_state_resume_cannot_use_uncommitted_markers(self):
        self.assertEqual(self.run_cli().returncode, 0)
        self.git("update-ref", "refs/heads/ralph/test", self.state()["starting_head"])
        before = (self.repo / "plan.json").read_bytes()
        result = self.run_cli("--resume")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("committed", result.stderr)
        self.assertEqual((self.repo / "plan.json").read_bytes(), before)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_resume_refuses_multiple_new_completion_markers(self):
        self.add_second_story()
        self.run_cli(action="false-complete")
        for story in self.plan["userStories"]:
            story["passes"] = True
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "unexpected multi-story delivery")
        result = self.run_cli("--resume")
        self.assertIn("exact committed selected-story transition", result.stderr)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_initial_dirty_work_refused_without_writes(self):
        for staged in (False, True):
            with self.subTest(staged=staged):
                case = RunnerTests()
                case.setUp()
                try:
                    work = case.repo / "user-work"
                    work.write_text("unrelated user work")
                    if staged:
                        case.git("add", "user-work")
                    index = (case.repo / ".git/index").read_bytes()
                    head = case.git("rev-parse", "HEAD")
                    for flags in ((), ("--resume",)):
                        result = case.run_cli(*flags)
                        self.assertIn("clean prepared", result.stderr)
                        self.assertFalse((case.root / "log").exists())
                        self.assertFalse((case.repo / ".git/ralph/state.json").exists())
                        self.assertEqual((case.repo / ".git/index").read_bytes(), index)
                        self.assertEqual(case.git("rev-parse", "HEAD"), head)
                        self.assertEqual(work.read_text(), "unrelated user work")
                finally:
                    case.doCleanups()

    def test_initial_plan_must_be_committed(self):
        self.plan["userStories"][0]["title"] = "uncommitted edit"
        self.write_plan()
        self.assertIn("clean prepared", self.run_cli("--resume").stderr)
        self.assertFalse((self.root / "log").exists())

    def test_linked_worktree_project_local_outcome(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "-qb", "ralph/linked", str(linked))
        self.repo = linked
        self.plan["branchName"] = "ralph/linked"
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "linked plan")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        call = json.loads((self.root / "log").read_text())
        outcome = Path(call["env"]["RALPH_OUTCOME_FILE"])
        self.assertEqual(outcome.parent, self.repo)
        self.assertRegex(outcome.name, r"^\.ralph-outcome-[0-9a-f]{32}\.json$")
        self.assertTrue(outcome.is_file())
        self.assertNotIn(".ralph-outcome-", self.git("ls-files"))
        state_dir = (self.repo / self.git("rev-parse", "--git-path", "ralph")).resolve()
        self.assertEqual(sorted(p.name for p in state_dir.iterdir()), ["lock", "state.json"])

    def test_only_strict_outcome_names_excluded(self):
        (self.repo / (".ralph-outcome-" + "a" * 32 + ".json")).write_text("old audit")
        (self.repo / ".ralph-outcome-user-notes.json").write_text("user work")
        result = self.run_cli()
        self.assertIn("clean prepared", result.stderr)
        self.assertFalse((self.root / "log").exists())

    def test_tracked_control_artifacts_refused(self):
        name = ".ralph-outcome-" + "b" * 32 + ".json"
        (self.repo / name).write_text("audit")
        self.git("add", name)
        self.assertIn("control artifacts", self.run_cli().stderr)
        self.assertFalse((self.root / "log").exists())

    def test_session_cannot_stage_or_commit_outcome(self):
        for action in ("track-outcome", "commit-outcome", "commit-remove-outcome"):
            with self.subTest(action=action):
                case = RunnerTests()
                case.setUp()
                try:
                    result = case.run_cli(action=action)
                    self.assertIn("control artifacts", result.stderr)
                    self.assertEqual(case.state()["status"], "blocked")
                    self.assertEqual(len((case.root / "log").read_text().splitlines()), 1)
                    self.assertIn("control artifacts", case.run_cli("--resume").stderr)
                finally:
                    case.doCleanups()

    def test_tracked_missing_stop_file_refused(self):
        stop = self.repo / ".ralph-stop"
        stop.touch()
        self.git("add", ".ralph-stop")
        self.git("commit", "-qm", "bad fixture control")
        stop.unlink()
        self.assertIn("control artifacts", self.run_cli().stderr)
        self.assertFalse((self.root / "log").exists())

    def test_retry_resume_cannot_hide_committed_then_removed_outcome(self):
        self.run_cli("--max-iterations", "1", action="retry")
        call = json.loads((self.root / "log").read_text())
        outcome = call["env"]["RALPH_OUTCOME_FILE"]
        self.git("add", outcome)
        self.git("commit", "-qm", "bad audit commit")
        self.git("rm", "--cached", outcome)
        self.git("commit", "-qm", "remove audit")
        result = self.run_cli("--resume")
        self.assertIn("control artifacts", result.stderr)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_old_outcomes_are_retained_and_excluded(self):
        old = self.repo / (".ralph-outcome-" + "d" * 32 + ".json")
        old.write_text("old audit")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(old.read_text(), "old audit")
        self.assertEqual(len(list(self.repo.glob(".ralph-outcome-*.json"))), 2)
        self.assertNotIn(".ralph-outcome-", self.git("ls-files"))

    def test_outcome_collision_refused(self):
        fixed_id = "c" * 32
        outcome = self.repo / f".ralph-outcome-{fixed_id}.json"
        outcome.write_text("old audit")
        bootstrap = "import runpy,uuid; from unittest.mock import patch; " \
            "p=patch.object(uuid,'uuid4',return_value=uuid.UUID(int=" + str(int(fixed_id, 16)) + ")); " \
            "p.start(); runpy.run_path(" + repr(str(RUNNER)) + ",run_name='__main__')"
        result = subprocess.run([sys.executable, "-c", bootstrap], cwd=self.repo,
                                env=self.env, capture_output=True, text=True)
        self.assertIn("outcome path already exists", result.stderr)
        self.assertFalse((self.root / "log").exists())
        self.assertEqual(outcome.read_text(), "old audit")

    def test_nested_history_rejected_without_leaking_or_overwrite(self):
        self.run_cli("--max-iterations", "1", action="retry")
        path = self.repo / ".git/ralph/state.json"
        state = self.state()
        state["stories"]["S1"]["history"] = [{"FAKE_SECRET_SENTINEL": "private"}]
        original = json.dumps(state)
        path.write_text(original)
        result = self.run_cli("--resume", action="vary")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed", result.stderr)
        self.assertNotIn("FAKE_SECRET_SENTINEL", result.stderr + result.stdout)
        self.assertEqual(path.read_text(), original)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_duplicate_json_key_error_is_secret_safe(self):
        self.run_cli(action="duplicate-secret")
        state = self.state()
        self.assertEqual(state["status"], "blocked")
        self.assertEqual(state["reason"], "invalid JSON in iteration outcome")
        self.assertNotIn("FAKE_SECRET_SENTINEL", json.dumps(state))

    def test_old_python_clear_error(self):
        with mock.patch.object(sys, "version_info", (3, 10, 0)), \
                mock.patch("sys.stderr") as stderr:
            with self.assertRaises(SystemExit) as exited:
                runpy.run_path(str(RUNNER), run_name="ralph_version_test")
            self.assertNotEqual(exited.exception.code, 0)
            self.assertIn("Python 3.11", "".join(str(c) for c in stderr.write.call_args_list))

    def test_unknown_exception_text_is_not_logged_or_persisted(self):
        bootstrap = "import runpy; from unittest.mock import patch; " \
            "ns=runpy.run_path(" + repr(str(RUNNER)) + "); " \
            "p=patch.dict(ns['main'].__globals__,supervise=lambda *a: " \
            "(_ for _ in ()).throw(OSError('FAKE_SECRET_SENTINEL'))); p.start(); " \
            "ns['main']()"
        # The external wrapper only prints the fixed Refusal; the runner persists
        # its sanitized reason before propagating it to this embedding caller.
        bootstrap = bootstrap.replace("ns['main']()", "\ntry: ns['main']()\nexcept Exception as error: print(str(error))")
        result = subprocess.run([sys.executable, "-c", bootstrap], cwd=self.repo,
                                env=self.env, capture_output=True, text=True)
        self.assertNotIn("FAKE_SECRET_SENTINEL", result.stdout + result.stderr)
        self.assertEqual(self.state()["reason"], "runner execution failed: I/O")
        self.assertNotIn("FAKE_SECRET_SENTINEL", json.dumps(self.state()))

    def test_committed_completion(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state()["status"], "completed")

    def test_outcome_failures_block_restart(self):
        for action in ("missing", "malformed", "stale", "wrong-story", "false-complete", "dirty-complete", "blocked", "stop", "fail"):
            with self.subTest(action=action):
                # Each case has an independent worktree and durable ledger.
                case = RunnerTests()
                case.setUp()
                try:
                    self.assertNotEqual(case.run_cli(action=action).returncode, 0)
                    calls = (case.root / "log").read_text()
                    self.assertNotEqual(case.run_cli().returncode, 0)
                    self.assertEqual((case.root / "log").read_text(), calls)
                finally:
                    case.doCleanups()

    def test_retry_persisted_snapshot_and_resume(self):
        self.assertNotEqual(self.run_cli("--max-iterations", "1", action="retry").returncode, 0)
        self.assertEqual(self.state()["status"], "ready")
        (self.repo / "work").write_text("user edit")
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)
        self.assertEqual(self.run_cli("--resume").returncode, 0)
        self.assertEqual(self.state()["stories"]["S1"]["retries"], 1)

    def test_repeated_approach_blocked(self):
        self.assertNotEqual(self.run_cli(action="repeat").returncode, 0)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 2)
        self.assertEqual(self.state()["status"], "blocked")

    def test_zero_budget_and_no_progress(self):
        self.assertNotEqual(self.run_cli("--max-story-retries", "0", action="retry").returncode, 0)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)
        self.assertNotEqual(self.run_cli("--resume").returncode, 0)

    def test_no_progress(self):
        result = self.run_cli(action="no-progress")
        self.assertIn("no measurable progress", result.stderr)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 1)

    def test_recovery_exhaustion_across_restarts(self):
        for _ in range(3):
            self.assertNotEqual(self.run_cli("--max-iterations", "1", action="vary").returncode, 0)
        self.assertEqual(self.state()["stories"]["S1"]["retries"], 2)
        self.assertEqual(self.state()["status"], "blocked")
        self.assertNotEqual(self.run_cli("--resume").returncode, 0)
        self.assertEqual(len((self.root / "log").read_text().splitlines()), 3)
        self.assertEqual(self.run_cli("--resume", "--max-story-retries", "3").returncode, 0)
        self.assertEqual(self.state()["stories"]["S1"]["retries"], 3)

    def test_staged_recovery_and_handoff(self):
        self.assertNotEqual(self.run_cli("--max-iterations", "1", action="staged").returncode, 0)
        self.assertIn("work", self.git("diff", "--cached", "--name-only"))
        self.assertEqual(self.run_cli().returncode, 0)
        calls = [json.loads(line) for line in (self.root / "log").read_text().splitlines()]
        self.assertNotEqual(calls[0]["env"]["RALPH_ITERATION_ID"], calls[1]["env"]["RALPH_ITERATION_ID"])
        for call in calls:
            context = call["argv"][-1]
            self.assertNotIn("User authorization handoff", context)
            self.assertNotIn("Outcome JSON:", context)
            self.assertEqual(context.splitlines()[0], "Ralph runtime context:")
            self.assertTrue(all(line.startswith("- ") for line in context.splitlines()[1:]))
            for field, value in (("Iteration ID", call["env"]["RALPH_ITERATION_ID"]),
                                 ("Selected story", call["env"]["RALPH_STORY_ID"]),
                                 ("Outcome file", call["env"]["RALPH_OUTCOME_FILE"])):
                self.assertIn(f"- {field}: {value}", context)
            self.assertNotIn("RALPH_STATE_DIR", call["env"])
        self.assertIn("Story attempt: 2; recoveries consumed: 1 of 2", calls[1]["argv"][-1])
        self.assertIn(calls[0]["env"]["RALPH_OUTCOME_FILE"], calls[1]["argv"][-1])

    def test_stop_precedes_completed_and_resume(self):
        self.assertEqual(self.run_cli().returncode, 0)
        (self.repo / ".ralph-stop").touch()
        self.assertNotEqual(self.run_cli("--resume").returncode, 0)
        self.assertTrue((self.repo / ".ralph-stop").exists())

    def test_plan_identity_mismatch_cannot_reset_budget(self):
        self.run_cli("--max-iterations", "1", action="retry")
        self.plan["userStories"][0]["title"] = "Different story"
        self.write_plan()
        self.assertIn("plan mismatch", self.run_cli("--resume").stderr)
        self.assertEqual(self.state()["stories"]["S1"]["attempts"], 1)

    def test_malformed_state_preserved(self):
        self.run_cli("--max-iterations", "1", action="retry")
        path = self.repo / ".git/ralph/state.json"
        path.write_text("{")
        self.assertNotEqual(self.run_cli("--resume").returncode, 0)
        self.assertEqual(path.read_text(), "{")

    def test_new_flag_bounds(self):
        for flag, values in (("--max-story-retries", ("-1", "6", "1.5", "abc")),
                             ("--iteration-timeout", ("-1", "86401", "1.5", "abc"))):
            for value in values:
                with self.subTest(flag=flag, value=value):
                    self.assertNotEqual(self.run_cli(flag, value).returncode, 0)
        self.assertFalse((self.root / "log").exists())

    def test_completed_plan_no_harness_and_no_worktree(self):
        self.plan["userStories"][0]["passes"] = True
        plain = self.root / "plain"
        plain.mkdir()
        (plain / "plan.json").write_text(json.dumps(self.plan))
        env = dict(self.env, PATH=os.environ["PATH"])
        result = subprocess.run([sys.executable, str(RUNNER)], cwd=plain, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "log").exists())

    def test_index_only_user_change_refused_without_mutation(self):
        self.run_cli("--max-iterations", "1", action="retry")
        self.git("add", "work")
        index_before = (self.repo / ".git/index").read_bytes()
        plan_before = (self.repo / "plan.json").read_bytes()
        result = self.run_cli()
        self.assertIn("snapshot mismatch", result.stderr)
        self.assertEqual((self.repo / ".git/index").read_bytes(), index_before)
        self.assertEqual((self.repo / "plan.json").read_bytes(), plan_before)

    def test_other_story_flip_rejected(self):
        self.add_second_story()
        self.assertIn("unexpected plan mutation", self.run_cli(action="other-story").stderr)

    def test_timeout(self):
        result = self.run_cli("--iteration-timeout", "1", action="sleep")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()["status"], "blocked")
        self.assertIn("timeout", result.stderr)
        child = int((self.root / "child").read_text())
        self.assert_process_dead(child)

    def assert_process_dead(self, pid):
        for _ in range(40):
            result = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
            if result.returncode or result.stdout.strip().startswith("Z"):
                return
            time.sleep(.05)
        self.fail(f"fixture child {pid} is still running")

    def test_signals_cleanup_managed_children(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            case = RunnerTests()
            case.setUp()
            proc = subprocess.Popen([sys.executable, str(RUNNER)], cwd=case.repo,
                                    env=dict(case.env, ACTION="sleep"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                for _ in range(100):
                    if (case.root / "child").exists(): break
                    time.sleep(.05)
                self.assertTrue((case.root / "child").exists())
                proc.send_signal(sig)
                self.assertNotEqual(proc.wait(timeout=10), 0)
                self.assert_process_dead(int((case.root / "child").read_text()))
                self.assertEqual(case.state()["status"], "blocked")
                self.assertEqual(len((case.root / "log").read_text().splitlines()), 1)
            finally:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=10)
                case.doCleanups()

    def test_crash_and_concurrent_lock(self):
        state = {}
        proc = subprocess.Popen([sys.executable, str(RUNNER)], cwd=self.repo,
                                env=dict(self.env, ACTION="sleep"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                if (self.root / "child").exists(): break
                time.sleep(.05)
            self.assertTrue((self.root / "child").exists())
            self.assertNotEqual(self.run_cli("--resume").returncode, 0)
            state = self.state()
            proc.kill()
            proc.wait()
            self.assertEqual(self.state()["status"], "running")
            self.assertNotEqual(self.run_cli().returncode, 0)
            self.assertIn("PID is still alive", self.run_cli("--resume").stderr)
        finally:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()
            # Only the process group recorded by this isolated test runner.
            if state.get("child_pid"):
                try: os.killpg(state["child_pid"], signal.SIGKILL)
                except ProcessLookupError: pass


if __name__ == "__main__":
    unittest.main()
