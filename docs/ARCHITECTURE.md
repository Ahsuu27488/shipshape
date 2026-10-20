# Architecture (as built)

## Layers (D-001)

```
skills/                      Layer 1: agent-neutral Agent Skills (any agent reads these)
  shipshape/                 router: memory first, understand first, tier, branch, plan, real tests, review,
                             memory, land, walkthrough; teaching levels; references/*.md
  shipshape-memory/          build the memory from real code (Mode A) / checkpoint (Mode B)
  shipshape-adopt/           set a repo up (existing or new) - assets/ = Layer 2 templates
  shipshape-unattended/      work alone: plan in repo, own branch, report, stop rules
  shipshape-checkup/         read-only score + next step
  shipshape-explain/         plain-words walkthrough of any change
skills/shipshape-adopt/assets/   Layer 2: copied into users' repos
  agents-md-block.md, CLAUDE.md, GEMINI.md, docs/*, shipshape/{config,context.sh,context.ps1,docs-gate.sh,gitignore},
  githooks/{commit-msg,pre-commit,pre-push}, ci/{python,node,generic,docs-gate-job}.yml, gitattributes, PR template
.claude-plugin/ hooks/ scripts/ agents/   Layer 3: the Claude Code plugin
tools/                       shipshape-run (unattended wrapper), render_assets.py, sync_eval_fixtures.py
tests/ evals/ compat/        unit/integration tests, Claude evals, cross-agent runs
```

## Code map

| Path | Responsibility |
|---|---|
| `skills/shipshape/SKILL.md` | The workflow every agent follows for code changes (steps 0-9, teaching, special situations) |
| `skills/shipshape/references/` | `plan`, `real-tests`, `review`, `land`, `walkthrough`, `live-safety`, `parallel`, `retro`, `why` (cards) |
| `skills/shipshape-adopt/assets/shipshape/context.sh` / `.ps1` | Session report: branch, commits, uncommitted, memory missing/stale, on-default-branch, unpushed, hooks inactive, unread unattended report; sources `context.local.sh` |
| `.../shipshape/docs-gate.sh` | Reads changed paths on stdin + `code_paths`/`docs_required` from `.shipshape/config`; exit 1 if code changed without the docs. Used by `commit-msg` and CI |
| `.../githooks/pre-commit` | Refuses commits on the default branch (not the first commit; `SHIPSHAPE_ALLOW_MAIN=1`), secret files and credential-looking lines (`shipshape:allow-secret` marker) |
| `.../githooks/pre-push` | Refuses updating or deleting the default branch on the remote; allows creating it |
| `scripts/session-start.sh` | Claude SessionStart: settings line, unattended note, new-project / setup offer (`auto_setup`), runs the repo's (or bundled) `context.sh`, injects STATUS + decision titles unless CLAUDE.md imports them |
| `scripts/guard-bash.sh` | Claude PreToolUse(Bash): ask/deny on commit/push to default branch (`git_guard`), force-push of main (always deny), `gh pr merge`, destructive commands (build-output cleanup exempt), `live_commands`; unattended = deny |
| `scripts/guard-files.sh` | Claude PreToolUse(Read/Edit/Write): deny secret files in unattended runs |
| `agents/shipshape-reviewer.md` | Fresh-context reviewer (Claude Code) |
| `tools/shipshape-run.sh` / `.ps1` | Unattended wrapper (D-007): worktree `auto/<date>-<slug>` → agent headless (`claude`/`codex`/`gemini`/`agy`/`cursor`/`copilot`/`custom`) → WIP commit → own checks → push + draft/ready PR → report to `.shipshape/last-report.md` |
| `tests/fixtures/tinyshop.sh` | The fixture project (modes `adopted` / `plain` / `empty`) for tests, evals, compat |
| `compat/run-case.sh`, `run-all.sh`, `lib.sh`, `cases/*` | Cross-agent runs graded on repo state |

## Settings

`.shipshape/config` (per repo, committed): `code_paths`, `docs_required`, `check_commands`, `default_branch`,
`live_commands`. `.shipshape/local.json` (git-ignored): teaching `level` and `seen` card counts. Claude plugin
`userConfig`: `teaching`, `git_guard`, `auto_setup` (exported to hooks as `CLAUDE_PLUGIN_OPTION_*`).
Environment: `SHIPSHAPE_UNATTENDED=1` (unattended rules + deny guards), `SHIPSHAPE_RUN=1` (the wrapper pushes/PRs),
`SHIPSHAPE_ALLOW_MAIN=1` (deliberate main commit/push), `SHIPSHAPE_NOTIFY`, `SHIPSHAPE_MAX_USD`, `SHIPSHAPE_AGENT_CMD`.

## Commands

```
python -m unittest discover -s tests -v
claude plugin validate --strict .
python tools/sync_eval_fixtures.py [--check]
sh compat/run-all.sh <agent> [case ...]
claude plugin eval . --scaffold --trust-plugin --model claude-sonnet-5-5 [--tag read-only]
python tools/render_assets.py sheet|export
```
