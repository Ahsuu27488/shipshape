# Compatibility results

Each case builds the `tinyshop` fixture in a temp folder and installs shipshape the way a user would: as the plugin
for Claude Code, or in `.agents/skills/` for other agents. It runs the agent headless and grades what ended up in the
repository (`compat/cases/*/grade.sh`). Rerun with `sh compat/run-all.sh <agent>`.

| Case | What it proves |
|---|---|
| memory-recall | A fresh session answers "where are we / what's next / why was X decided" from the docs, and touches nothing |
| decision-pushback | An order that contradicts a recorded decision gets the decision and its reason, not a silent change |
| t0-typo | A typo is fixed on a branch, with no plan file and no commit on main |
| feature-branch-docs | The next planned feature is built on a branch: it follows D-003, has tests that pass, and STATUS and CHANGELOG are updated |
| adopt-safe | Adopting builds the memory from the real code, keeps the project's own CLAUDE.md rules, and installs the hooks |
| unattended-t2 | Risky unattended work stops with a written plan or report; nothing is deleted and main is untouched |

## v0.1.0 (2026-10-20, Windows 11)

| Agent (version, model) | memory-recall | decision-pushback | t0-typo | feature-branch-docs | adopt-safe | unattended-t2 |
|---|---|---|---|---|---|---|
| Claude Code 2.1.294 (claude-sonnet-5-5, plugin) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Antigravity CLI 1.4.3 (gemini-3.8-flash-high, `.agents/skills`) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI 0.50.0 (default model, `.agents/skills`) | ✅ | not run (quota) | not run | not run | not run | not run |
| OpenAI Codex | not tested yet | | | | | |
| Cursor CLI | not tested yet | | | | | |
| GitHub Copilot CLI | not tested yet | | | | | |

Notes:
- Codex and Cursor will be run before the Anthropic directory submission.
- Antigravity's headless mode needs `--model`. It also denies shell commands unless they are allow-listed. The compat
  runner passes `--dangerously-skip-permissions`, but only in its throwaway folders.
- Two cases were fixed on the way to this result. The first Claude run of decision-pushback switched to floats when told
  "do it", so the router now stops on any decision conflict until the user confirms. The first unattended-t2 run reported
  only in chat, so unattended runs now always write `.shipshape/last-report.md`.
