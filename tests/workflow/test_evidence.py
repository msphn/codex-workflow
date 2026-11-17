"""Exercise observable Git evidence behavior with disposable, offline fixtures."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "workflow_evidence.py"
SPEC = importlib.util.spec_from_file_location("workflow_evidence", SCRIPT)
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="orchestrator-evidence-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.env = patch.dict(os.environ, {
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        })
        self.env.start()
        self.addCleanup(self.env.stop)
        self.git("init", "--template=", "--initial-branch=develop")
        self.git("config", "commit.gpgsign", "false")
        self.write("source.txt", "base\n")
        self.commit("base", "source.txt")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("update-ref", "refs/remotes/origin/develop", self.base)
        self.git("switch", "-c", "feature/TEST-1")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout

    def write(self, name, content):
        (self.repo / name).write_text(content)

    def commit(self, message, *paths):
        self.git("add", "--", *paths)
        self.git("commit", "-m", message)

    def capture(self, *paths):
        return evidence.capture(self.repo, self.base, paths or ["source.txt"], "origin/develop")

    def test_full_range_includes_earlier_commits(self):
        self.write("source.txt", "first change\n")
        self.commit("first", "source.txt")
        first = self.git("rev-parse", "HEAD").strip()
        self.write("second.txt", "second change\n")
        self.commit("second", "second.txt")
        snapshot = self.capture("source.txt", "second.txt")
        self.assertEqual([first, snapshot["head"]], snapshot["commits"])
        self.assertEqual(["second.txt", "source.txt"], snapshot["committed_paths"])
        self.assertEqual(self.base, snapshot["base"])

    def test_owner_index_and_worktree_preserved(self):
        self.write("owner.txt", "owner staged\n")
        self.git("add", "owner.txt")
        self.write("owner.txt", "owner unstaged\n")
        self.write("source.txt", "ticket\n")
        before_index = (self.repo / ".git/index").read_bytes()
        before_diff = self.git("diff", "--cached")
        before_head = self.git("rev-parse", "HEAD")
        snapshot = self.capture("source.txt", "owner.txt")
        self.assertTrue(any("owner.txt" in item for item in snapshot["index"]))
        self.assertEqual("unchanged", evidence.check(snapshot)["status"])
        self.assertEqual(before_index, (self.repo / ".git/index").read_bytes())
        self.assertEqual(before_diff, self.git("diff", "--cached"))
        self.assertEqual(before_head, self.git("rev-parse", "HEAD"))
        self.assertEqual("owner unstaged\n", (self.repo / "owner.txt").read_text())

    def test_already_dirty_file_change_invalidates_without_head_change(self):
        self.write("source.txt", "first dirty version\n")
        before = self.capture()
        self.write("source.txt", "second dirty version\n")
        after = self.capture()
        self.assertEqual(before["head"], after["head"])
        self.assertEqual(before["status"], after["status"])
        self.assertIn("files", evidence.check(before)["changed_fields"])

    def test_staging_changes_invalidates_snapshot(self):
        self.write("source.txt", "changed\n")
        before = self.capture()
        self.git("add", "source.txt")
        self.assertIn("index", evidence.check(before)["changed_fields"])

    def test_untracked_and_deleted_files(self):
        self.write("new file.txt", "new\n")
        (self.repo / "source.txt").unlink()
        before = self.capture("new file.txt", "source.txt")
        self.assertEqual({"kind": "missing"}, before["files"]["source.txt"])
        self.write("new file.txt", "changed new file\n")
        self.assertIn("files", evidence.check(before)["changed_fields"])

    def test_executable_mode_and_symlink_target(self):
        (self.repo / "link").symlink_to("source.txt")
        before = self.capture("source.txt", "link")
        (self.repo / "source.txt").chmod(0o755)
        self.assertIn("files", evidence.check(before)["changed_fields"])
        (self.repo / "link").unlink()
        (self.repo / "link").symlink_to("missing")
        self.assertEqual("missing", self.capture("link")["files"]["link"]["target"])

    def test_rejects_paths_outside_checkout_and_directories(self):
        (self.repo / "outside").symlink_to(self.root, target_is_directory=True)
        for path in ["../secret", str(self.root / "secret"), ".git/config", ".", "outside/secret"]:
            with self.subTest(path=path), self.assertRaises(evidence.EvidenceError):
                self.capture(path)

    def test_remote_base_advance_is_visible_without_checkout_changes(self):
        before = self.capture()
        # Construct an independent upstream child without switching or fetching.
        tree = self.git("rev-parse", "HEAD^{tree}").strip()
        upstream = self.git("commit-tree", tree, "-p", self.base, "-m", "upstream").strip()
        self.git("update-ref", "refs/remotes/origin/develop", upstream)
        after = self.capture()
        self.assertFalse(after["remote_base_is_ancestor"])
        self.assertEqual(before["head"], after["head"])
        self.assertIn("remote_base_sha", evidence.check(before)["changed_fields"])

    def test_hook_mutations_in_successful_and_failed_commits(self):
        hook = self.repo / ".git/hooks/pre-commit"
        hook.parent.mkdir(exist_ok=True)
        for exit_code in (1, 0):
            with self.subTest(exit_code=exit_code):
                self.write("source.txt", "validated\n")
                self.git("add", "source.txt")
                before = self.capture()
                hook.write_text('#!/bin/sh\nprintf "hook changed\\n" > source.txt\ngit add -- source.txt\nexit ' + str(exit_code) + '\n')
                hook.chmod(0o755)
                result = subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "hook test"],
                                        capture_output=True)
                self.assertEqual(exit_code, result.returncode)
                self.assertIn("files", evidence.check(before)["changed_fields"])
                self.assertEqual(exit_code == 1, before["head"] == self.capture()["head"])

    def test_concurrent_change_rejected(self):
        original = evidence.read_state
        calls = 0

        def moving_state(*args):
            nonlocal calls
            result = original(*args)
            calls += 1
            if calls == 1:
                self.write("source.txt", "concurrent edit\n")
            return result

        with patch.object(evidence, "read_state", side_effect=moving_state):
            with self.assertRaisesRegex(evidence.EvidenceError, "Checkout changed"):
                self.capture()

    def test_cli_exit_codes(self):
        snapshot_path = self.root / "evidence.json"
        snapshot_path.write_text(json.dumps(self.capture()))

        def run(*args):
            return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True)

        self.assertEqual(0, run("check", str(snapshot_path)).returncode)
        self.write("source.txt", "changed\n")
        self.assertEqual(1, run("check", str(snapshot_path)).returncode)
        snapshot_path.write_text("not json")
        self.assertEqual(2, run("check", str(snapshot_path)).returncode)
        self.assertEqual(2, run("snapshot", "--repo", str(self.repo), "--base", "--invalid",
                                "--paths", "source.txt").returncode)


if __name__ == "__main__":
    unittest.main()
