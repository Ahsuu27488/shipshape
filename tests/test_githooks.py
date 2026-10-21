"""The repo-level guards every agent and human share: the real .githooks scripts in a real git repository."""
from __future__ import annotations

import unittest

from helpers import ASSETS, RepoTestCase


class CommitRules(RepoTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.make_fixture("adopted")
        self.git("switch", "-q", "-c", "feat/discounts", check=True)

    def commit(self, msg: str = "change") -> object:
        return self.git("commit", "-q", "-m", msg)

    def test_code_without_docs_is_rejected(self):
        self.write("tinyshop/discount.py", "PERCENT_MAX = 100\n")
        self.git("add", "-A", check=True)
        r = self.commit("add discount module")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("project memory was not updated", r.stderr)
        self.assertIn("docs/STATUS.md", r.stderr)
        self.assertIn("tinyshop/discount.py", r.stderr)

    def test_code_with_docs_is_accepted(self):
        self.write("tinyshop/discount.py", "PERCENT_MAX = 100\n")
        self.write("docs/STATUS.md", (self.repo / "docs/STATUS.md").read_text(encoding="utf-8") + "\n- discount module\n")
        self.write("docs/CHANGELOG.md", "# Changelog\n\n## 2026-10-20\n- discount module\n")
        self.git("add", "-A", check=True)
        self.assertEqual(self.commit("add discount module").returncode, 0)

    def test_no_docs_marker_bypasses(self):
        self.write("tinyshop/money.py", "# formatting only\n" + (self.repo / "tinyshop/money.py").read_text(encoding="utf-8"))
        self.git("add", "-A", check=True)
        self.assertEqual(self.commit("comment only [no-docs]").returncode, 0)

    def test_docs_only_change_needs_nothing(self):
        self.write("README.md", "# tinyshop\n\nCustomers receive a receipt.\n")
        self.git("add", "-A", check=True)
        self.assertEqual(self.commit("fix typo").returncode, 0)

    def test_commit_on_main_is_refused(self):
        self.git("switch", "-q", "main", check=True)
        self.write("README.md", "# tinyshop\n")
        self.git("add", "-A", check=True)
        r = self.commit("typo on main")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no commits directly on 'main'", r.stderr)

    def test_commit_on_main_allowed_with_explicit_override(self):
        self.git("switch", "-q", "main", check=True)
        self.write("README.md", "# tinyshop\n")
        self.git("add", "-A", check=True)
        env = dict(self.env, SHIPSHAPE_ALLOW_MAIN="1")
        self.assertEqual(self.git("commit", "-q", "-m", "release [no-docs]", env=env).returncode, 0)

    def test_secret_file_is_refused(self):
        self.write(".env.local", "TOKEN=abc\n")
        self.git("add", "-f", ".env.local", check=True)
        r = self.commit("oops [no-docs]")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(".env.local", r.stderr)

    def test_env_example_is_fine(self):
        self.write(".env.example", "TOKEN=\n")
        self.git("add", ".env.example", check=True)
        self.assertEqual(self.commit("example env [no-docs]").returncode, 0)

    def test_secret_line_is_refused_and_value_not_echoed(self):
        key = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        self.write("config_local.py", f'TOKEN = "{key}"\n')
        self.git("add", "-A", check=True)
        r = self.commit("config [no-docs]")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("looks like a real credential", r.stderr)
        self.assertNotIn(key, r.stderr)

    def test_marked_fake_secret_is_allowed(self):
        key = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        self.write("test_fixture.py", f'TOKEN = "{key}"  # shipshape:allow-secret\n')
        self.git("add", "-A", check=True)
        self.assertEqual(self.commit("fixture [no-docs]").returncode, 0)


class FirstCommit(RepoTestCase):
    def test_first_commit_of_a_new_repo_may_go_on_main(self):
        # a brand-new repo that set up shipshape before its first commit
        new = self.tmp / "new"
        new.mkdir()
        self.repo = new
        self.git("init", "-q", "-b", "main", check=True)
        (new / ".githooks").mkdir()
        for hook in ("pre-commit", "commit-msg", "pre-push"):
            target = new / ".githooks" / hook
            target.write_bytes((ASSETS / "githooks" / hook).read_bytes())
            target.chmod(0o755)  # git skips non-executable hooks on Linux/macOS
        self.git("config", "core.hooksPath", ".githooks", check=True)
        self.write("README.md", "# new\n")
        self.git("add", "-A", check=True)
        self.assertEqual(self.git("commit", "-q", "-m", "first").returncode, 0)
        self.write("README.md", "# new project\n")
        self.git("add", "-A", check=True)
        self.assertNotEqual(self.git("commit", "-q", "-m", "second").returncode, 0)


class PushRules(RepoTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.make_fixture("adopted")
        self.remote = self.tmp / "remote.git"
        self.git("init", "-q", "--bare", str(self.remote), cwd=self.tmp, check=True)
        self.git("remote", "add", "origin", str(self.remote), check=True)

    def test_first_push_of_main_creates_it(self):
        self.assertEqual(self.git("push", "-q", "origin", "main").returncode, 0)

    def test_pushing_main_again_is_refused(self):
        self.git("push", "-q", "origin", "main", check=True)
        env = dict(self.env, SHIPSHAPE_ALLOW_MAIN="1")
        self.write("README.md", "# tinyshop\n")
        self.git("add", "-A", check=True)
        self.git("commit", "-q", "-m", "direct [no-docs]", env=env, check=True)
        r = self.git("push", "-q", "origin", "main")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("only changes through a pull request", r.stderr)

    def test_feature_branch_push_is_fine(self):
        self.git("push", "-q", "origin", "main", check=True)
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.write("README.md", "# tinyshop\n")
        self.git("add", "-A", check=True)
        self.git("commit", "-q", "-m", "readme", check=True)
        self.assertEqual(self.git("push", "-q", "-u", "origin", "feat/x").returncode, 0)

    def test_deleting_main_on_the_remote_is_refused(self):
        self.git("push", "-q", "origin", "main", check=True)
        self.assertNotEqual(self.git("push", "-q", "origin", "--delete", "main").returncode, 0)


class DocsGateForCI(RepoTestCase):
    def test_reads_a_file_list_like_ci_does(self):
        self.make_fixture("adopted")
        gate = self.repo / ".shipshape" / "docs-gate.sh"
        self.assertNotEqual(self.sh(gate, input="tinyshop/cart.py\n").returncode, 0)
        ok = self.sh(gate, input="tinyshop/cart.py\ndocs/STATUS.md\ndocs/CHANGELOG.md\n")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(self.sh(gate, input="README.md\n").returncode, 0)

    def test_crlf_config_still_works(self):
        self.make_fixture("adopted")
        cfg = self.repo / ".shipshape" / "config"
        cfg.write_bytes(cfg.read_bytes().replace(b"\n", b"\r\n"))
        gate = self.repo / ".shipshape" / "docs-gate.sh"
        self.assertNotEqual(self.sh(gate, input="tinyshop/cart.py\r\n").returncode, 0)
        self.assertEqual(self.sh(gate, input="tinyshop/cart.py\r\ndocs/STATUS.md\r\ndocs/CHANGELOG.md\r\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
