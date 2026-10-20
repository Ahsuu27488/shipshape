"""The skills follow the open Agent Skills spec (agentskills.io) and stay agent-neutral and within the
directory's limits, so every agent can load them."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from helpers import ROOT

SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Tool names that exist only in one vendor's agent. The skills must say "ask the user", not name a tool.
VENDOR_TOOLS = ["AskUserQuestion", "TodoWrite", "ExitPlanMode", "EnterPlanMode", "activate_skill", "Task tool",
                "Agent tool", "SlashCommand", "${CLAUDE_PLUGIN_ROOT}", "CLAUDE_PLUGIN_DATA"]


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    end = text.index("\n---\n", 4)
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[end + 5:]


class SkillSpec(unittest.TestCase):
    def skill_dirs(self) -> list[Path]:
        dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
        self.assertGreaterEqual(len(dirs), 6)
        return dirs

    def test_frontmatter_follows_the_spec(self):
        for d in self.skill_dirs():
            with self.subTest(skill=d.name):
                meta, body = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
                self.assertEqual(meta.get("name"), d.name, "name must match the folder")
                self.assertRegex(meta["name"], NAME_RE)
                self.assertLessEqual(len(meta["name"]), 64)
                self.assertTrue(meta["name"].startswith("shipshape"), "skill folders are global in .agents/skills")
                desc = meta.get("description", "")
                self.assertTrue(0 < len(desc) <= 1024, f"description length {len(desc)}")
                self.assertIn("Use ", desc, "description must say when to use it")
                self.assertEqual(meta.get("license"), "MIT")
                self.assertLess(len(body.splitlines()), 500)

    def test_no_vendor_only_tool_names(self):
        for path in SKILLS.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for tool in VENDOR_TOOLS:
                with self.subTest(file=str(path.relative_to(ROOT)), tool=tool):
                    self.assertNotIn(tool, text)

    def test_relative_links_resolve(self):
        link = re.compile(r"`((?:\.\./)?[a-z0-9-]+(?:/[A-Za-z0-9._-]+)*\.md)`")
        for skill_md in SKILLS.glob("*/SKILL.md"):
            text = skill_md.read_text(encoding="utf-8")
            for ref in link.findall(text):
                if ref.startswith(("docs/", "AGENTS", "CLAUDE", "GEMINI", ".shipshape")) or "/" not in ref and ref.isupper():
                    continue
                if not (ref.startswith("references/") or ref.startswith("../")):
                    continue
                with self.subTest(skill=skill_md.parent.name, ref=ref):
                    self.assertTrue((skill_md.parent / ref).exists(), f"{ref} not found")

    def test_assets_the_adopt_skill_names_exist(self):
        adopt = (SKILLS / "shipshape-adopt" / "SKILL.md").read_text(encoding="utf-8")
        for ref in re.findall(r"`assets/([A-Za-z0-9_./-]+)`", adopt):
            if "*" in ref:
                continue
            with self.subTest(asset=ref):
                self.assertTrue((SKILLS / "shipshape-adopt" / "assets" / ref).exists(), ref)


class DirectoryLimits(unittest.TestCase):
    """Anthropic's directory: files < 256 KiB (images aside), <= 512 files, no binaries, no top-level bin/."""

    def tracked_files(self) -> list[Path]:
        skip = {".git", "__pycache__", "results", "runs", "drafts"}
        return [p for p in ROOT.rglob("*") if p.is_file() and not (set(p.relative_to(ROOT).parts) & skip)]

    def test_sizes_and_types(self):
        files = self.tracked_files()
        self.assertLessEqual(len(files), 512)
        allowed_binary = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
        for f in files:
            with self.subTest(file=str(f.relative_to(ROOT))):
                if f.suffix.lower() in allowed_binary:
                    continue
                self.assertLess(f.stat().st_size, 256 * 1024)
                f.read_text(encoding="utf-8")  # text only
        self.assertFalse((ROOT / "bin").exists(), "a top-level bin/ makes claude.ai refuse the plugin")

    def test_manifest_and_marketplace(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], "shipshape")
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(market["plugins"][0]["source"], "./")
        self.assertRegex(plugin["version"], r"^\d+\.\d+\.\d+$")
        for skill_md in SKILLS.glob("*/SKILL.md"):
            meta, _ = frontmatter(skill_md.read_text(encoding="utf-8"))
        version_lines = [l for p in SKILLS.glob("*/SKILL.md") for l in p.read_text(encoding="utf-8").splitlines()
                         if l.strip().startswith("version:")]
        for line in version_lines:
            self.assertIn(plugin["version"], line, "skill metadata.version must match plugin.json")

    def test_hook_commands_reference_existing_scripts(self):
        hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        for event in hooks["hooks"].values():
            for group in event:
                for h in group["hooks"]:
                    script = re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"]+)", h["command"]).group(1)
                    with self.subTest(script=script):
                        self.assertTrue((ROOT / script).exists())

    def test_hooks_and_scripts_are_executable_in_git(self):
        import subprocess
        out = subprocess.run(["git", "ls-files", "-s", "--", ".githooks", "scripts", "tools", "compat",
                              "skills/shipshape-adopt/assets/githooks", "skills/shipshape-adopt/assets/shipshape"],
                             cwd=ROOT, capture_output=True, text=True).stdout
        for line in out.splitlines():
            mode, _, _, path = line.split(None, 3)
            if path.endswith((".sh",)) or "/githooks/" in path or path.startswith(".githooks/"):
                with self.subTest(path=path):
                    self.assertEqual(mode, "100755", "git skips non-executable hooks on Linux/macOS")

    def test_shell_scripts_have_lf_endings(self):
        for f in list(ROOT.glob("scripts/*.sh")) + list(ROOT.glob("tools/*.sh")) \
                + list((SKILLS / "shipshape-adopt" / "assets" / "githooks").iterdir()) \
                + list((SKILLS / "shipshape-adopt" / "assets" / "shipshape").glob("*.sh")):
            with self.subTest(file=f.name):
                self.assertNotIn(b"\r\n", f.read_bytes())


if __name__ == "__main__":
    unittest.main()
