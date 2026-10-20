"""The Claude Code layer: the real SessionStart and PreToolUse scripts, fed the JSON Claude Code sends."""
from __future__ import annotations

import json
import unittest

from helpers import SCRIPTS, RepoTestCase, hook_input


class GuardBash(RepoTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.make_fixture("adopted")

    def decide(self, command: str, **env: str) -> str | None:
        e = dict(self.env, CLAUDE_PROJECT_DIR=str(self.repo), **env)
        r = self.sh(SCRIPTS / "guard-bash.sh", input=hook_input(command=command), env=e)
        self.assertEqual(r.returncode, 0, r.stderr)
        if not r.stdout.strip():
            return None
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]

    def test_commit_on_main_asks_by_default(self):
        self.assertEqual(self.decide('git commit -m "x"'), "ask")

    def test_commit_on_main_blocked_or_off(self):
        self.assertEqual(self.decide('git commit -m "x"', CLAUDE_PLUGIN_OPTION_GIT_GUARD="block"), "deny")
        self.assertIsNone(self.decide('git commit -m "x"', CLAUDE_PLUGIN_OPTION_GIT_GUARD="off"))

    def test_commit_on_a_branch_is_left_alone(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.assertIsNone(self.decide('git add -A && git commit -m "x"'))

    def test_push_to_main(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.assertEqual(self.decide("git push origin main"), "ask")
        self.assertIsNone(self.decide("git push -u origin feat/x"))

    def test_bare_push_while_on_main_asks(self):
        self.assertEqual(self.decide("git push"), "ask")

    def test_force_push_of_main_is_always_denied(self):
        self.assertEqual(self.decide("git push --force origin main", CLAUDE_PLUGIN_OPTION_GIT_GUARD="off"), "deny")

    def test_merge_asks_interactive_denies_unattended(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.assertEqual(self.decide("gh pr merge 12 --squash"), "ask")
        self.assertEqual(self.decide("gh pr merge 12 --squash", SHIPSHAPE_UNATTENDED="1"), "deny")

    def test_unattended_never_commits_on_main(self):
        self.assertEqual(self.decide('git commit -m "x"', SHIPSHAPE_UNATTENDED="1"), "deny")

    def test_destructive_commands(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        for cmd in ("rm -rf src", "git reset --hard HEAD~3", "git clean -fdx", "sqlite3 app.db 'DROP TABLE orders'",
                    "git push origin --delete feat/old"):
            self.assertEqual(self.decide(cmd), "ask", cmd)
            self.assertEqual(self.decide(cmd, SHIPSHAPE_UNATTENDED="1"), "deny", cmd)

    def test_cleaning_build_output_is_fine(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.assertIsNone(self.decide("rm -rf node_modules dist"))
        self.assertIsNone(self.decide("rm -rf .pytest_cache && python -m pytest"))

    def test_live_commands_from_config(self):
        self.git("switch", "-q", "-c", "feat/x", check=True)
        cfg = self.repo / ".shipshape" / "config"
        cfg.write_text(cfg.read_text(encoding="utf-8").replace("live_commands=", "live_commands=fly deploy|kubectl apply"),
                       encoding="utf-8")
        self.assertEqual(self.decide("fly deploy --app shop"), "ask")
        self.assertEqual(self.decide("fly deploy --app shop", SHIPSHAPE_UNATTENDED="1"), "deny")
        self.assertIsNone(self.decide("fly status"))

    def test_ordinary_commands_get_no_opinion(self):
        for cmd in ("python -m unittest -q", "git status", "git log --oneline -8", "ls -la", "git diff main...HEAD"):
            self.assertIsNone(self.decide(cmd), cmd)

    def test_garbage_input_never_breaks_the_tool_call(self):
        e = dict(self.env, CLAUDE_PROJECT_DIR=str(self.repo))
        r = self.sh(SCRIPTS / "guard-bash.sh", input="not json at all", env=e)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "")


class GuardFiles(RepoTestCase):
    def decide(self, path: str, **env: str) -> str | None:
        r = self.sh(SCRIPTS / "guard-files.sh", input=hook_input(file_path=path), env=dict(self.env, **env), cwd=self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] if r.stdout.strip() else None

    def test_secrets_only_blocked_unattended(self):
        self.assertIsNone(self.decide("/repo/.env"))
        self.assertEqual(self.decide("/repo/.env", SHIPSHAPE_UNATTENDED="1"), "deny")
        self.assertEqual(self.decide("C:\\\\repo\\\\data\\\\youtube-cookies.txt", SHIPSHAPE_UNATTENDED="1"), "deny")
        self.assertIsNone(self.decide("/repo/.env.example", SHIPSHAPE_UNATTENDED="1"))
        self.assertIsNone(self.decide("/repo/src/app.py", SHIPSHAPE_UNATTENDED="1"))


class SessionStart(RepoTestCase):
    def start(self, folder, **opts: str) -> str:
        data = self.tmp / "plugin-data"
        env = dict(self.env, CLAUDE_PROJECT_DIR=str(folder), CLAUDE_PLUGIN_DATA=str(data), **opts)
        r = self.sh(SCRIPTS / "session-start.sh", env=env, cwd=folder)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_adopted_repo_gets_state_and_memory(self):
        self.make_fixture("adopted")
        out = self.start(self.repo)
        self.assertIn("Teaching level: working", out)
        self.assertIn("## Project state (shipshape session report)", out)
        self.assertIn("You are on the default branch 'main'", out)
        # CLAUDE.md imports the docs, so the hook does not duplicate them
        self.assertIn("CLAUDE.md imports docs/STATUS.md", out)
        self.assertIn("read them now", out)

    def test_memory_is_injected_when_claude_md_does_not_import_it(self):
        self.make_fixture("adopted")
        (self.repo / "CLAUDE.md").write_text("# tinyshop\n", encoding="utf-8")
        out = self.start(self.repo)
        self.assertIn("## Project memory: docs/STATUS.md", out)
        self.assertIn("Percentage discount codes", out)
        self.assertIn("**D-002 Money is stored and computed as integer cents", out)
        self.assertIn("**D-003 Discount codes apply to the subtotal before tax", out)

    def test_repo_without_memory_ask_mode_offers_once(self):
        self.make_fixture("plain")
        out = self.start(self.repo)
        self.assertIn("Offer once", out)
        self.assertIn("declined-setup.txt", out)

    def test_declined_repo_is_not_offered_again(self):
        self.make_fixture("plain")
        data = self.tmp / "plugin-data"
        data.mkdir()
        top = self.git("rev-parse", "--show-toplevel", check=True).stdout.strip()
        (data / "declined-setup.txt").write_text(top + "\n", encoding="utf-8")
        out = self.start(self.repo)
        self.assertIn("declined setup for this folder earlier", out)
        self.assertNotIn("Offer once", out)

    def test_repo_without_memory_auto_mode_sets_up(self):
        self.make_fixture("plain")
        out = self.start(self.repo, CLAUDE_PLUGIN_OPTION_AUTO_SETUP="auto")
        self.assertIn("Memory setup is AUTO", out)
        self.assertIn("shipshape-adopt", out)

    def test_empty_folder_is_a_new_project(self):
        empty = self.tmp / "newproj"
        empty.mkdir()
        out = self.start(empty)
        self.assertIn("this is a NEW project", out)

    def test_block_guard_on_main(self):
        self.make_fixture("adopted")
        self.assertIn("Git guard is BLOCK", self.start(self.repo, CLAUDE_PLUGIN_OPTION_GIT_GUARD="block"))

    def test_unattended_contract(self):
        self.make_fixture("adopted")
        self.assertIn("UNATTENDED RUN", self.start(self.repo, SHIPSHAPE_UNATTENDED="1"))


if __name__ == "__main__":
    unittest.main()
