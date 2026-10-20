"""The session report (.shipshape/context.sh): what every new agent session learns before writing code."""
from __future__ import annotations

import shutil
import unittest

from helpers import RepoTestCase


class SessionReport(RepoTestCase):
    def report(self) -> str:
        r = self.sh(self.repo / ".shipshape" / "context.sh")
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_in_sync_on_a_branch(self):
        self.make_fixture("adopted")
        self.git("switch", "-q", "-c", "feat/x", check=True)
        out = self.report()
        self.assertIn("**Branch:** feat/x", out)
        self.assertIn("in sync with the latest code commit", out)
        self.assertIn("read docs/STATUS.md, docs/DECISIONS.md and docs/ARCHITECTURE.md", out)

    def test_warns_on_the_default_branch(self):
        self.make_fixture("adopted")
        self.assertIn("You are on the default branch 'main'", self.report())

    def test_warns_when_docs_fall_behind_the_code(self):
        self.make_fixture("adopted")
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.write("tinyshop/cart.py", (self.repo / "tinyshop/cart.py").read_text(encoding="utf-8") + "\n# tweak\n")
        self.git("add", "-A", check=True)
        self.git("commit", "-q", "-m", "tweak cart [no-docs]", check=True)
        out = self.report()
        self.assertIn("docs/STATUS.md is older than 1 code commit(s)", out)
        self.assertIn("tweak cart", out)

    def test_warns_about_uncommitted_code_without_status(self):
        self.make_fixture("adopted")
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.write("tinyshop/money.py", "# wip\n")
        out = self.report()
        self.assertIn("Uncommitted changes (1)", out)
        self.assertIn("Uncommitted code changes exist but docs/STATUS.md is untouched", out)

    def test_warns_when_hooks_are_not_active(self):
        self.make_fixture("adopted")
        self.git("config", "--unset", "core.hooksPath", check=True)
        self.assertIn("git hooks are NOT active", self.report())

    def test_warns_about_unpushed_commits(self):
        self.make_fixture("adopted")
        remote = self.tmp / "r.git"
        self.git("init", "-q", "--bare", str(remote), cwd=self.tmp, check=True)
        self.git("remote", "add", "origin", str(remote), check=True)
        self.git("push", "-q", "-u", "origin", "main", check=True)
        self.git("switch", "-q", "-c", "feat/x", check=True)
        self.git("push", "-q", "-u", "origin", "feat/x", check=True)
        self.write("README.md", "# tinyshop\n")
        self.git("add", "-A", check=True)
        self.git("commit", "-q", "-m", "readme", check=True)
        self.assertIn("1 commit(s) are not pushed yet", self.report())

    def test_missing_memory_is_reported(self):
        self.make_fixture("plain")
        (self.repo / ".shipshape").mkdir()
        from helpers import ASSETS
        shutil.copy(ASSETS / "shipshape" / "context.sh", self.repo / ".shipshape" / "context.sh")
        self.assertIn("Project memory is missing: docs/STATUS.md", self.report())

    def test_unread_unattended_report_is_flagged(self):
        self.make_fixture("adopted")
        self.write(".shipshape/last-report.md", "# ✅ Done: x\n")
        self.assertIn("An unattended run left a report", self.report())

    def test_project_extras_are_appended(self):
        self.make_fixture("adopted")
        self.write(".shipshape/context.local.sh", 'echo "**Servers:** api :8000 running"\n')
        self.assertIn("**Servers:** api :8000 running", self.report())


if __name__ == "__main__":
    unittest.main()
