"""Shared helpers: run the real shell scripts in throwaway git repositories, isolated from the user's git config."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "skills" / "shipshape-adopt" / "assets"
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "tinyshop.sh"
SH = shutil.which("sh") or shutil.which("bash")


def clean_env(**extra: str) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "CLAUDE_", "SHIPSHAPE_"))}
    home = tempfile.mkdtemp(prefix="ss-home-")
    env.update(
        HOME=home,
        USERPROFILE=home,
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_NAME="Test",
        GIT_AUTHOR_EMAIL="test@example.com",
        GIT_COMMITTER_NAME="Test",
        GIT_COMMITTER_EMAIL="test@example.com",
    )
    env.update(extra)
    return env


class RepoTestCase(unittest.TestCase):
    """Each test gets a fresh temp folder and an isolated git environment."""

    def setUp(self) -> None:
        if not SH:
            self.skipTest("sh is not installed")
        self.tmp = Path(tempfile.mkdtemp(prefix="ss-test-"))
        self.env = clean_env()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cmd(self, *args: str, cwd: Path | None = None, input: str | None = None, env: dict | None = None,
                check: bool = False) -> subprocess.CompletedProcess:
        result = subprocess.run(
            list(args), cwd=cwd or self.repo, input=input, env=env or self.env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if check and result.returncode != 0:
            raise AssertionError(f"{args} failed ({result.returncode}):\n{result.stdout}\n{result.stderr}")
        return result

    def git(self, *args: str, **kw) -> subprocess.CompletedProcess:
        return self.run_cmd("git", *args, **kw)

    def sh(self, script: Path | str, *args: str, **kw) -> subprocess.CompletedProcess:
        return self.run_cmd(SH, str(script), *args, **kw)

    def make_fixture(self, mode: str = "adopted", name: str = "repo") -> Path:
        self.repo = self.tmp / name
        self.run_cmd(SH, str(FIXTURE), str(self.repo), mode, str(ROOT), cwd=self.tmp, check=True)
        return self.repo

    def write(self, rel: str, text: str) -> Path:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path


def hook_input(command: str | None = None, file_path: str | None = None) -> str:
    tool_input: dict = {}
    if command is not None:
        tool_input = {"command": command, "description": "run it"}
        name = "Bash"
    else:
        tool_input = {"file_path": file_path}
        name = "Read"
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": name, "tool_input": tool_input})
