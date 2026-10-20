# Privacy policy

_Last updated: 20 October 2026_

shipshape is an open-source set of instructions (Agent Skills), shell scripts and a Claude Code plugin. It runs
entirely on your own computer, inside the coding agent you already use. This policy explains what it does with data.

## What shipshape collects

Nothing. shipshape has no servers, accounts, analytics or telemetry, and its scripts make no network requests of
their own.

## Where your data goes

Your coding agent (Claude Code, Codex, Cursor, Copilot, Gemini CLI, Antigravity or another) reads shipshape's
instructions and your project files and sends them to its own vendor, under that vendor's terms. shipshape does not
change where that data goes. The instructions tell the agent never to read, print or commit secrets such as `.env`
files and keys, and in unattended runs the Claude Code plugin blocks opening them.

When you ask for it, the workflow runs `git` and GitHub's `gh` CLI with your own sign-in: `git push` sends your branch
to your remote, and `gh pr create` opens a pull request there. `tools/shipshape-run.sh` does both at the end of an
unattended run that you started.

## What shipshape stores on your computer

- In your project (committed, so your team shares them): `docs/` memory files, `AGENTS.md` / `CLAUDE.md` /
  `GEMINI.md`, `.shipshape/config` and scripts, `.githooks/`, CI files.
- In your project (git-ignored, personal): `.shipshape/local.json` (your teaching level and which explanations you
  have seen), `.shipshape/last-report.md` and `.shipshape/runs/` (unattended run logs and reports).
- Claude Code plugin only: `declined-setup.txt` in the plugin's data folder (`~/.claude/plugins/data/...`), a list of
  folders where you said no to setting up the memory, so it is not offered again.
- `shipshape-run` worktrees next to your repository, in `<repo>.shipshape/`.

You can delete any of these at any time.

## Contact

Questions: open an issue at https://github.com/Ahsuu27488/shipshape/issues.
