"""tools/shipshape-run.sh, the unattended wrapper, driven end to end with a scripted stand-in agent."""
from __future__ import annotations

import unittest

from helpers import ROOT, RepoTestCase

RUN = ROOT / "tools" / "shipshape-run.sh"

GOOD_AGENT = r"""
set -e
test "$SHIPSHAPE_UNATTENDED" = 1
branch=$(git branch --show-current)
mkdir -p docs/plans
printf '# Plan: discount\nTier: T1\n' > docs/plans/2026-10-20-discount.md
git add docs/plans && git commit -q -m "plan: discount codes [no-docs]"
printf 'def discount_cents(subtotal, percent):\n    return subtotal * percent // 100\n' > tinyshop/discount.py
printf '\n- discount_cents added\n' >> docs/STATUS.md
printf '\n## 2026-10-20\n- discount_cents\n' >> docs/CHANGELOG.md
git add -A && git commit -q -m "Add discount_cents (D-003: rounded down)"
printf '# ✅ Done: discount codes\n\n**Result:** added discount_cents on %s\n' "$branch" > .shipshape/last-report.md
"""

LAZY_AGENT = r"""
printf 'x = 1\n' > tinyshop/half_done.py
"""

BREAKING_AGENT = r"""
set -e
printf 'raise SystemExit("broken")\n' > tinyshop/__init__.py
printf '\n- broke it\n' >> docs/STATUS.md
printf '\n- broke it\n' >> docs/CHANGELOG.md
git add -A && git commit -q -m "change init"
printf '# ✅ Done: all good\n' > .shipshape/last-report.md
"""


class Wrapper(RepoTestCase):
    def run_agent(self, script: str, task: str = "add discount codes") -> object:
        env = dict(self.env, SHIPSHAPE_AGENT_CMD=script)
        return self.sh(RUN, "--agent", "custom", "--no-pr", "--keep", task, env=env)

    def setUp(self) -> None:
        super().setUp()
        self.make_fixture("adopted")
        self.main_head = self.git("rev-parse", "main", check=True).stdout.strip()

    def branches(self) -> list[str]:
        out = self.git("branch", "--format=%(refname:short)", check=True).stdout
        return [b for b in out.split() if b.startswith("auto/")]

    def test_good_run_lands_on_its_own_branch_and_is_verified(self):
        r = self.run_agent(GOOD_AGENT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.git("rev-parse", "main", check=True).stdout.strip(), self.main_head, "main untouched")
        [branch] = self.branches()
        self.assertTrue(branch.startswith("auto/"))
        self.assertIn("add-discount-codes", branch)
        log = self.git("log", "--oneline", f"main..{branch}", check=True).stdout
        self.assertIn("plan: discount codes", log)
        report = (self.repo / ".shipshape" / "last-report.md").read_text(encoding="utf-8")
        self.assertTrue(report.startswith("# ✅ Done"))
        self.assertIn("## Independent checks (shipshape-run)", report)
        self.assertIn("python -m unittest -q` → passed", report)
        self.assertIn("2 commit(s)", report)

    def test_agent_that_leaves_no_report_and_uncommitted_work(self):
        r = self.run_agent(LAZY_AGENT)
        self.assertNotEqual(r.returncode, 0)
        [branch] = self.branches()
        log = self.git("log", "--oneline", f"main..{branch}", check=True).stdout
        self.assertIn("wip: unattended run ended with uncommitted work", log)
        report = (self.repo / ".shipshape" / "last-report.md").read_text(encoding="utf-8")
        self.assertTrue(report.startswith("# ⛔ Stopped: the agent left no report"))

    def test_wrapper_does_not_trust_the_agents_claim(self):
        r = self.run_agent(BREAKING_AGENT)
        self.assertNotEqual(r.returncode, 0, "checks failed, so the run is not 'done'")
        report = (self.repo / ".shipshape" / "last-report.md").read_text(encoding="utf-8")
        self.assertIn("→ FAILED", report)
        self.assertEqual(self.git("rev-parse", "main", check=True).stdout.strip(), self.main_head)

    def test_dry_run_prints_each_agent_command(self):
        for agent, needle in (("claude", "--permission-mode auto"), ("codex", "--sandbox workspace-write"),
                              ("agy", "--mode accept-edits"), ("cursor", "--force"), ("gemini", "--approval-mode")):
            r = self.sh(RUN, "--agent", agent, "--dry-run", "add a health endpoint")
            with self.subTest(agent=agent):
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertIn(needle, r.stdout)
                self.assertIn("shipshape-unattended", r.stdout)
                self.assertIn("auto/", r.stdout)


if __name__ == "__main__":
    unittest.main()
