# Contributing to shipshape

Thanks for helping. The most valuable contributions are **compat results from agents not yet verified** and
**real incidents** that a habit would have prevented (they become why cards).

## The repo follows its own rules

Read `AGENTS.md` and `docs/STATUS.md` first. Work on a branch, update `docs/STATUS.md` and `docs/CHANGELOG.md` with
any change to skills, scripts or tools (the `commit-msg` hook checks), and open a pull request. Enable the hooks once
per clone: `git config core.hooksPath .githooks`.

## Checks

```bash
python -m unittest discover -s tests -v       # hooks, session report, Claude hooks, wrapper, skill spec
claude plugin validate --strict .              # plugin + marketplace manifests
python tools/sync_eval_fixtures.py --check     # eval fixtures in sync with tests/fixtures/tinyshop.sh
```

## Verifying an agent (compat)

1. Install the agent's CLI and sign in.
2. `sh compat/run-all.sh <agent>` (agents: claude, codex, agy, gemini, cursor, copilot). Each case builds a fresh
   fixture project in a temp folder, installs the skills the way a user would, runs the agent headless with approvals
   off (throwaway folder only), and grades what ended up in the repository.
3. Add a row to `compat/RESULTS.md` with the date, the agent's version and the results, and attach the log from
   `compat/results/<agent>.log` to your PR.

## Claude evals

`claude plugin eval . --scaffold --trust-plugin` runs `evals/` (cases tagged `needs-bash` need a sandbox: Linux,
macOS or WSL2). Edit fixtures only in `tests/fixtures/tinyshop.sh`, then run `python tools/sync_eval_fixtures.py`.

## Writing skills

Skills follow the open [Agent Skills spec](https://agentskills.io/specification) and must work in every agent: no
vendor-specific tool names (the tests check), plain verbs ("ask the user"), under 500 lines, details in `references/`.
