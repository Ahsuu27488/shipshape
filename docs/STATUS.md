# Project Status

> Current truth only. History in CHANGELOG.md, reasons in DECISIONS.md.

**Last updated:** 2026-10-20 · **Code at:** first commit (v0.1.0, not pushed, not published)
**In one line:** v0.1 is built and its unit tests pass; the cross-agent release gate is partly run.

## What works (verified)

- 60 unit/integration tests pass on Windows (`python -m unittest discover -s tests`): the real git hooks, the session
  report, the Claude hooks, the unattended wrapper (with a stand-in agent), and the skill spec and limits.
- `claude plugin validate --strict` passes for the marketplace and the plugin.
- In a real headless Claude Code session on Windows, the plugin's SessionStart and PreToolUse hooks fire: the memory
  loads, and a commit on main is stopped by the guard.
- Compat (real agents, fixture repo; logs in `compat/results/`, git-ignored):
  - **Claude** (sonnet-5-5): memory-recall, t0-typo, feature-branch-docs and adopt-safe PASS. decision-pushback FAILED
    (it cited D-002 but still switched to floats because the prompt said "do it"; the rule was tightened afterwards,
    not re-run yet). unattended-t2 was not run (the script was edited mid-run).
  - **Antigravity** (agy 1.4.3): memory-recall PASS. The other cases failed on the runner, not the skills (missing
    `--model`, then permissions); both are fixed and the cases have not been re-run yet.
  - **Gemini CLI** 0.50: memory-recall PASS.
  - **Codex, Cursor:** not installed on this PC, so not run.

## In progress

- Logo: three drafts in `assets/drafts/` (sheet.png). Ahsan picks A/B/C. `assets/logo.svg` and the PNGs are
  concept A for now.

## Known gaps

1. `claude plugin eval` cannot sign in from the desktop app on this PC (D-008). `evals/` is untested end to end; run it
   in CI with an API key, or after `claude setup-token`.
2. The release gate (Claude + Codex + Antigravity + Cursor pass the core cases) has not been met: Codex and Cursor
   aren't installed, and the Antigravity cases need a re-run.
3. `context.ps1` is untested (the tests run the `sh` version).
4. `tools/shipshape-run.sh` has been tested only with a stand-in agent, not a real overnight run.

## Next

1. Re-run the compat suite: `sh compat/run-all.sh claude decision-pushback unattended-t2`, then `sh compat/run-all.sh agy`.
2. Install and sign in to Codex and Cursor's CLI (Ahsan), then `sh compat/run-all.sh codex` and `cursor`.
   Write the results to `compat/RESULTS.md`.
3. Swap in the logo Ahsan picks (`python tools/render_assets.py export`).
4. Create the GitHub repo `Ahsuu27488/shipshape` and push (Ahsan's go-ahead), then submit to the directory.
5. Ahsan's own install: the plugin at user scope with `auto_setup=auto`.

## How to run and check

- `python -m unittest discover -s tests -q`, then `claude plugin validate --strict .`, then `python tools/sync_eval_fixtures.py --check`
