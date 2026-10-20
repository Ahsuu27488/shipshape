# Changelog

> Newest first. Each entry: date, commit (or "uncommitted"), what changed, and for fixes the root cause.

## 2026-10-20 · v0.1.0 (first build)

- Six agent-neutral skills: `shipshape` (router), `shipshape-memory`, `shipshape-adopt` (existing and new projects),
  `shipshape-unattended`, `shipshape-checkup`, `shipshape-explain`; references for planning, real-path tests, review,
  landing, walkthroughs, live safety, parallel work, retros, and 14 why cards.
- Repo assets written by adopt: memory doc templates, AGENTS.md block, CLAUDE.md / GEMINI.md, `.shipshape/` (config,
  session report in sh and PowerShell, docs gate), git hooks (`commit-msg`, `pre-commit`, `pre-push`), CI templates
  with a docs-gate job, PR template, `.gitattributes` for LF scripts.
- Claude Code plugin: SessionStart memory + state + setup offer, Bash and file guards, reviewer agent, settings
  (`teaching`, `git_guard`, `auto_setup`).
- `tools/shipshape-run` unattended wrapper for claude, codex, gemini, agy, cursor, copilot.
- Tests: unit/integration tests against the real scripts and git; 9 Claude eval cases; 6 cross-agent compat cases.
- Found while building: (1) Windows checkouts turn hook scripts to CRLF and `sh` then fails, so adopt now writes
  `.gitattributes` and every script strips `\r` from config values; (2) `claude plugin eval` child sessions can't use
  the desktop app's sign-in here, and the user's `ANTHROPIC_MODEL` points at a non-Claude model (D-008).
