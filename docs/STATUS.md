# Project Status

> Current truth only. History in CHANGELOG.md, reasons in DECISIONS.md.

**Last updated:** 2026-10-20 · **Code at:** github.com/Ahsuu27488/shipshape `main` (public)
**In one line:** v0.1 is built and has passed its release gate: Claude Code and Antigravity pass all 6 compat cases.

## What works (verified)

- 61 unit and integration tests pass on Windows and Ubuntu (CI; macOS CI is off: its runner never started) (`python -m unittest discover -s tests`). They run the real git
  hooks, the session report, the Claude hooks, the unattended wrapper (with a stand-in agent), and the skill-spec and
  limits checks.
- `claude plugin validate --strict` passes for the marketplace and the plugin.
- In a real headless Claude Code session on Windows, the SessionStart and PreToolUse hooks fire: the memory loads, and
  the guard stops a commit on main.
- **Release gate (Ahsan: Claude + Antigravity) met:** all 6 compat cases pass on Claude Code 2.1.294 (sonnet-5-5) and
  on Antigravity CLI 1.4.3 (gemini-3.8-flash-high). Gemini CLI 0.50 passed memory-recall. See `compat/RESULTS.md`.
- Logo: concept A ("checked sail"), chosen by Ahsan; `assets/` holds the SVG and the PNG exports.

## In progress

- **Anthropic directory:** v0.1.0 (`f5c3b08`) submitted 2026-10-21. It is in the security scan, then goes to a reviewer
  because of 5 policy holds: local hooks/scripts, image files, a credential mention, and a name similar to
  `fisky2340/shipshape`. Updates come from the scheduled check every 6 hours (no webhook). Auto-publish is on for later versions.
  Portal: claude.ai/directory/manage/plugins/a83f9202-d1ad-4e79-a624-1101ea09d01f

## Known gaps

1. `claude plugin eval` cannot sign in from the desktop app on this PC (D-008), so `evals/` hasn't been run end to end.
   Run it in CI with an API key, or after `claude setup-token`.
2. Codex, Cursor and Copilot are not tested yet (not installed here). Gemini CLI has passed memory-recall only.
3. `context.ps1` is untested (the tests run the `sh` version).
4. `tools/shipshape-run.sh` has been tested only with a stand-in agent, not with a real overnight run.

## Next

1. Done: GitHub social preview set.
2. Done: submitted to the Anthropic directory (see In progress). When approved, press Publish there.
3. Done: Ahsan's own install, the plugin at user scope with `auto_setup=auto`, `teaching=working`, `git_guard=ask`.
4. Run the compat cases on Codex and Cursor, and `evals/` with a working login (Ahsan chose to submit first).
5. One real overnight `shipshape-run` on a small repo.

## How to run and check

- `python -m unittest discover -s tests -q`, then `claude plugin validate --strict .`, then `python tools/sync_eval_fixtures.py --check`
