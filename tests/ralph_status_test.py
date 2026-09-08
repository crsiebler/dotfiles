"""Read-only status checks using isolated Git repositories and a fake harness."""

import fcntl
import json
from pathlib import Path
import os
import runpy
import unittest
from unittest import mock
from typing import Any

import ralph_runner_test as fixtures


class StatusTests(unittest.TestCase):
    root: Path
    repo: Path
    plan: dict[str, Any]
    env: dict[str, str]
    setUp = fixtures.RunnerTests.setUp
    git = fixtures.RunnerTests.git
    write_plan = fixtures.RunnerTests.write_plan
    run_cli = fixtures.RunnerTests.run_cli
    state = fixtures.RunnerTests.state
    add_second_story = fixtures.RunnerTests.add_second_story

    def inventory(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns,
                                               p.stat().st_ctime_ns)
                for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def status(self, *args):
        before = self.inventory()
        result = self.run_cli("--status", *args)
        self.assertEqual(self.inventory(), before)
        return result

    def test_fresh_no_control_creation(self):
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Next action: ready to start", result.stdout)
        self.assertFalse((self.repo / ".git/ralph").exists())
        self.assertFalse((self.root / "log").exists())

    def test_options_rejected(self):
        for args in (("--resume",), ("--mode", "fast"), ("--model", "secret"),
                     ("--max-iterations", "1"), ("--max-story-retries", "2"),
                     ("--iteration-timeout", "1"), ("--auto",)):
            result = self.status(*args)
            self.assertEqual(result.returncode, 1)
            self.assertIn("--status cannot be combined", result.stderr)
        self.assertEqual(self.status("--help").returncode, 0)

    def test_missing_corrupt_and_stop(self):
        (self.repo / "plan.json").rename(self.repo / "saved-plan")
        self.assertIn("plan unavailable", self.status().stdout)
        (self.repo / "plan.json").write_text("{")
        (self.repo / ".ralph-stop").write_text("FAKE_SECRET_SENTINEL")
        result = self.status()
        self.assertEqual(result.returncode, 0)
        self.assertIn("stop file present", result.stdout)
        self.assertNotIn("FAKE_SECRET_SENTINEL", result.stdout + result.stderr)

    def test_dirty_start(self):
        (self.repo / "work").write_text("user work")
        self.git("add", "work")
        self.assertIn("needs reconciliation", self.status().stdout)

    def test_retry_and_exhaustion(self):
        self.run_cli("--max-iterations", "1", action="retry")
        result = self.status()
        self.assertIn("Last outcome: retryable", result.stdout)
        self.assertIn("Remaining: 2", result.stdout)
        self.assertIn("ready to resume after explicit approval", result.stdout)
        self.run_cli("--max-story-retries", "0", action="retry")
        self.assertIn("recovery budget exhausted", self.status().stdout)

    def test_next_story_has_fresh_budget(self):
        self.add_second_story()
        self.run_cli("--max-iterations", "1", "--max-story-retries", "0")
        result = self.status()
        self.assertIn("Current story: S1", result.stdout)
        self.assertIn("Next story: S2", result.stdout)
        self.assertIn("Attempts: 0", result.stdout)
        self.assertIn("ready to resume after explicit approval", result.stdout)

    def test_blocked_and_secret_fields(self):
        self.run_cli(action="blocked")
        path = self.repo / self.git("rev-parse", "--git-path", "ralph/state.json")
        state = self.state()
        state.update(reason="FAKE_SECRET_SENTINEL", unknown="FAKE_SECRET_SENTINEL")
        path.write_text(json.dumps(state))
        result = self.status()
        self.assertIn("needs reconciliation", result.stdout)
        self.assertIn("Last outcome: blocked", result.stdout)
        self.assertNotIn("FAKE_SECRET_SENTINEL", result.stdout + result.stderr)
        path.write_text("{")
        self.assertIn("state unavailable", self.status().stdout)

    def test_completed_and_provisional(self):
        self.run_cli(action="false-complete")
        self.assertIn("needs reconciliation", self.status().stdout)
        self.git("add", "plan.json")
        self.git("commit", "-qm", "reconcile")
        self.run_cli("--resume")
        self.assertIn("Next action: completed", self.status().stdout)

    def test_stale_malformed_symlink_outcome(self):
        self.run_cli("--max-iterations", "1", action="retry")
        path = self.repo / (".ralph-outcome-" + self.state()["iteration_id"] + ".json")
        for content in ("{", json.dumps(dict(version=1, iteration_id="old",
                                            story_id="S1", status="completed"))):
            path.write_text(content)
            self.assertIn("Last outcome: unavailable", self.status().stdout)
        path.rename(self.repo / "saved-outcome")
        path.symlink_to(self.repo / "saved-outcome")
        self.assertIn("Last outcome: unavailable", self.status().stdout)

    def test_lock_active(self):
        control = self.repo / ".git/ralph"
        control.mkdir()
        with (control / "lock").open("w") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.status()
            self.assertIn("State: active", result.stdout)
            self.assertIn("do not reconcile while active", result.stdout)
            self.assertNotIn("Next action: ready", result.stdout)

    def test_linked_worktree(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "-qb", "ralph/linked", str(linked))
        self.repo = linked
        self.plan["branchName"] = "ralph/linked"
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "linked plan")
        result = self.status()
        self.assertIn("Next action: ready to start", result.stdout)
        self.assertIn("worktrees/linked/ralph/state.json", result.stdout)

    def test_identity_candidate_and_rewritten_head(self):
        self.run_cli("--max-iterations", "1", action="retry")
        (self.repo / "work").write_text("changed")
        self.assertIn("candidate or completion mismatch", self.status().stdout)
        self.plan["userStories"][0]["title"] = "changed identity"
        self.write_plan()
        self.assertIn("plan identity mismatch", self.status().stdout)
        self.plan["userStories"][0]["title"] = "Test"
        self.write_plan()
        orphan = self.git("commit-tree", "HEAD^{tree}", "-m", "unrelated")
        self.git("update-ref", "refs/heads/ralph/test", orphan)
        self.assertIn("rewritten HEAD", self.status().stdout)

    def test_oversized_and_missing_outcomes(self):
        self.run_cli("--max-iterations", "1", action="retry")
        path = self.repo / (".ralph-outcome-" + self.state()["iteration_id"] + ".json")
        path.write_bytes(b" " * (4 * 1024 * 1024 + 1))
        self.assertIn("Last outcome: unavailable", self.status().stdout)
        path.rename(self.root / "oversized")
        self.assertIn("Last outcome: unavailable", self.status().stdout)
        self.assertIn("needs reconciliation", self.status().stdout)

    def test_status_never_calls_execution_or_mutating_apis(self):
        namespace = runpy.run_path(str(fixtures.RUNNER))
        entry = namespace["status_report"]
        previous = Path.cwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(self.repo)
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.dict(entry.__globals__, {
                    key: mock.Mock(side_effect=AssertionError(key))
                    for key in ("atomic", "execute", "supervise", "alive")}), \
                mock.patch("os.fsync", side_effect=AssertionError("fsync")), \
                mock.patch("os.kill", side_effect=AssertionError("kill")), \
                mock.patch("os.killpg", side_effect=AssertionError("killpg")), \
                mock.patch("pathlib.Path.mkdir", side_effect=AssertionError("mkdir")), \
                mock.patch("builtins.print") as output:
            self.assertEqual(entry(), 0)
            self.assertTrue(any("ready to start" in str(c) for c in output.call_args_list))

    def test_changed_snapshot_never_ready(self):
        namespace = runpy.run_path(str(fixtures.RUNNER))
        entry = namespace["status_report"]
        previous = Path.cwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(self.repo)
        original = namespace["snapshot"]
        calls = 0

        def changing_snapshot():
            nonlocal calls
            result = original()
            calls += 1
            if calls > 1:
                result["candidate"] = "0" * 64
            return result

        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.dict(entry.__globals__, snapshot=changing_snapshot), \
                mock.patch("builtins.print") as output:
            self.assertEqual(entry(), 0)
            rendered = "\n".join(str(c) for c in output.call_args_list)
            self.assertIn("snapshot changed during inspection", rendered)
            self.assertNotIn("Next action: ready", rendered)

    def test_running_and_unsafe_control(self):
        self.run_cli(action="blocked")
        path = self.repo / self.git("rev-parse", "--git-path", "ralph/state.json")
        state = self.state()
        state["status"] = "running"
        path.write_text(json.dumps(state))
        self.assertIn("running or blocked state", self.status().stdout)
        path.rename(self.root / "saved-state")
        path.symlink_to(self.root / "saved-state")
        self.assertIn("state unavailable", self.status().stdout)

    def test_arbitrary_identifiers_withheld(self):
        self.plan["userStories"][0]["id"] = "FAKE_SECRET_SENTINEL\nState: ready"
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "identifier fixture")
        self.run_cli(action="blocked")
        result = self.status()
        self.assertNotIn("FAKE_SECRET_SENTINEL", result.stdout + result.stderr)
        self.assertIn("Current story: withheld", result.stdout)

    def test_complete_plan_without_ledger_does_not_claim_delivery(self):
        self.plan["userStories"][0]["passes"] = True
        self.write_plan()
        self.git("add", "plan.json")
        self.git("commit", "-qm", "complete fixture")
        self.assertIn("delivery not proven without ledger", self.status().stdout)


if __name__ == "__main__":
    unittest.main()
