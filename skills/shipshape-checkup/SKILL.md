---
name: shipshape-checkup
description: Scores a repository against professional engineering habits (memory docs, branches, CI, hooks, real-path tests, PR template, decision log, live-safety) and recommends the single most valuable next step, read-only. Use when the user asks how professional or healthy their repo is, what to improve next, for a checkup, or before adopting shipshape.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
---

# shipshape-checkup: where does this repo stand?

Read-only: change nothing. Check each habit with commands and file reads, not assumptions.

| # | Habit | How to check | Points |
|---|---|---|---|
| 1 | Memory docs exist | `docs/STATUS.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `CHANGELOG.md` | 2 |
| 2 | Memory is current | STATUS committed after the latest code commit (`.shipshape/context.sh` reports it) | 2 |
| 3 | Decisions have reasons | DECISIONS entries are numbered and each has a *Why* | 1 |
| 4 | Agents load the memory | AGENTS.md (and CLAUDE.md / GEMINI.md if used) point to the docs | 1 |
| 5 | Work happens on branches | recent history has merge/PR commits, not only direct commits on main (`git log --merges`, `--first-parent`) | 1 |
| 6 | Hooks guard the rules | `.githooks/` with commit-msg + pre-commit + pre-push, and `core.hooksPath` set in this clone | 1 |
| 7 | CI runs the checks | `.github/workflows/*` (or other CI) runs tests on pull requests | 2 |
| 8 | Tests exist and pass | run them; at least one test exercises the real code path of the main feature | 2 |
| 9 | PR template | `.github/pull_request_template.md` | 1 |
| 10 | Default branch protected | `gh api repos/<owner>/<repo>/branches/<main>/protection` (or note: not available on this plan) | 1 |
| 11 | No secrets in the repo | no `.env`/keys tracked (`git ls-files`), `.gitignore` covers them | 1 |
| 12 | Live systems documented | if anything is live: STATUS has a "Live state" section and `live_commands` is set | 1 |

Report:

```
shipshape checkup: <score>/16
✅ <habits met>
❌ <habits missing, one line each, with the evidence>
Next step: <the ONE change with the most value for the least effort, and how (usually: shipshape-adopt)>
```

In learning level, add one sentence of why for each ❌ (from `../shipshape/references/why.md`).
