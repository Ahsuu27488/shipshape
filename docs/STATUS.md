# Project Status

> Current truth only. History in CHANGELOG.md, reasons in DECISIONS.md.

**Last updated:** 2026-10-20 · **Code at:** github.com/Ahsuu27488/shipshape `main` (public)
**In one line:** v0.1 is built and has passed its release gate: Claude Code and Antigravity pass all 6 compat cases.

## What works (verified)

- 61 unit and integration tests pass on Windows, Ubuntu and macOS (CI) (`python -m unittest discover -s tests`). They run the real git
  hooks, the session report, the Claude hooks, the unattended wrapper (with a stand-in agent), and the skill-spec and
  limits checks.
- `claude plugin validate --strict` passes for the marketplace and the plugin.
- In a real headless Claude Code session on Windows, the SessionStart and PreToolUse hooks fire: the memory loads, and
  the guard stops a commit on main.
- **Release gate (Ahsan: Claude + Antigravity) met:** all 6 compat cases pass on Claude Code 2.1.294 (sonnet-5-5) and
  on Antigravity CLI 1.4.3 (gemini-3.8-flash-high). Gemini CLI 0.50 passed memory-recall. See `compat/RESULTS.md`.
- Logo: concept A ("checked sail"), chosen by Ahsan; `assets/` holds the SVG and the PNG exports.

## In progress

- Nothing.

## Known gaps

1. `claude plugin eval` cannot sign in from the desktop app on this PC (D-008), so `evals/` hasn't been run end to end.
   Run it in CI with an API key, or after `claude setup-token`.
2. Codex, Cursor and Copilot are not tested yet (not installed here). Gemini CLI has passed memory-recall only.
3. `context.ps1` is untested (the tests run the `sh` version).
4. `tools/shipshape-run.sh` has been tested only with a stand-in agent, not with a real overnight run.

## Next

1. Set the GitHub social preview (`assets/social-preview.png`; Settings → Social preview, by hand or in Chrome).
2. Submit to the Anthropic directory (claude.ai/directory/manage).
3. Done: Ahsan's own install, the plugin at user scope with `auto_setup=auto`, `teaching=working`, `git_guard=ask`.
4. Before the Anthropic directory submission: run the compat cases on Codex and Cursor, run `evals/` with a working
   login, and validate in the directory portal.
5. One real overnight `shipshape-run` on a small repo.

## How to run and check

- `python -m unittest discover -s tests -q`, then `claude plugin validate --strict .`, then `python tools/sync_eval_fixtures.py --check`
