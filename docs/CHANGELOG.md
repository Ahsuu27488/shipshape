# Changelog

> Newest first. Each entry: date, commit (or "uncommitted"), what changed, and for fixes the root cause.

## 2026-10-20 · executable hooks (fix)

- Hook and script files are now committed as executable (100755), and adopt makes them executable on disk and in
  git. Root cause: on Windows, git doesn't record the executable bit, so the files were stored as 100644, and git on
  Linux and macOS silently skips a hook that isn't executable. Found by the first GitHub CI run (ubuntu and macOS
  failed, Windows passed). A new test checks the mode of every hook and script in the git index.
- Published to the public repository github.com/Ahsuu27488/shipshape. The internal plan and private project
  details were kept out of it.

## 2026-10-20 · release gate (branch feat/v0.1-release-gate)

- The release gate passed: all 6 compat cases on Claude Code and Antigravity CLI (`compat/RESULTS.md`).
- Router: a request that contradicts a recorded decision stops before any edit until the user confirms, even after
  "do it". Root cause: on its first run, Claude cited D-002 and then still switched the cart to floats.
- Unattended: every run writes `.shipshape/last-report.md`, even one that changed nothing, and a decision conflict stops
  after the plan. Root cause: Claude stopped correctly but reported only in chat output, which nobody reads overnight.
- Compat runner: Antigravity is given `--model`. Each case runs from a snapshot of `run-case.sh`, so editing the script
  can't break a batch in progress. Fixture repos get a git identity.
- `tools/shipshape-run.sh`: added `SHIPSHAPE_AGENT_ARGS` for extra agent flags, and a hint when a headless agent was
  denied permissions.
- The logo is concept A ("checked sail"), chosen by Ahsan.

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
