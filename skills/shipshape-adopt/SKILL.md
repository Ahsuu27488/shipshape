---
name: shipshape-adopt
description: Sets a project up to be worked on professionally by any coding agent - project memory docs built from the real code (STATUS, DECISIONS, ARCHITECTURE, CHANGELOG), an AGENTS.md / CLAUDE.md / GEMINI.md rules block, git hooks that guard main and require doc updates, a session report script, CI and a pull-request template - delivered on a branch as a reviewable pull request. Also starts brand-new projects this way. Use when the user asks to set up, adopt or install shipshape, "make this repo professional", start a new project, or when the shipshape skill finds a project with no memory docs.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
---

# shipshape-adopt: set the project up once, so it stays professional

What this installs keeps working for every agent and every human who touches the repo, even without shipshape:
the docs carry the memory, the git hooks and CI enforce the rules. Everything goes in **on a branch, as a
pull request**, so the human reviews it like any other change.

Templates are in this skill's `assets/` folder. Read each one and write it into the project; never overwrite
an existing file. **Merge** into it instead, and leave anything the project already does better alone.

## 1. Survey (read-only)

Find and note:
- Is it a git repository? Default branch (`git symbolic-ref refs/remotes/origin/HEAD`, else `main`/`master`)?
  Remote? Uncommitted work (never touch it)?
- Stack and the **real** check commands: what actually exists in `package.json` scripts, `pyproject.toml`,
  `Makefile`, CI. Run them once to see they work.
- The code folders (for `code_paths`): `src/`, `app/`, `lib/`, `backend/`, `frontend/`, `cmd/`, `scripts/`…
- Existing agent and memory files: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules/`, `.github/
  copilot-instructions.md`, `docs/`, a `.githooks/` folder or `core.hooksPath`, existing CI, a project
  checkpoint skill. **Existing decisions and docs win**; you add what is missing.
- Is anything **live** (a deployed service, a bot, production data)? Then the adopt PR itself must not change
  runtime behaviour, and `live_commands` in the config should list the commands that touch it.

Show the human a short report: what exists, what you will add, what you will leave alone. Mode `ask`
(default): wait for "go". Mode `auto`: say what you are doing and continue.

## 2. Branch

`git switch -c chore/adopt-shipshape` (from an up-to-date default branch). A repository with no commits yet:
see "New project" below.

## 3. Memory docs

Follow the `shipshape-memory` skill, **Mode A**, to build `docs/STATUS.md`, `DECISIONS.md`, `ARCHITECTURE.md`
and `CHANGELOG.md` from the real code, using `assets/docs/*` as the templates. Add `docs/plans/README.md` from
`assets/docs/plans-README.md`.

## 4. Rules for every agent

- **AGENTS.md** (read by Codex, Cursor, Copilot, Antigravity and others): insert `assets/agents-md-block.md`
  between its markers. If AGENTS.md exists, add the block at the top and keep everything else. If the block is
  already there, replace only the text between the markers.
- **CLAUDE.md** (Claude Code): if missing, write `assets/CLAUDE.md`. If present, add the lines `@AGENTS.md`,
  `@docs/STATUS.md`, `@docs/DECISIONS.md` and `@docs/ARCHITECTURE.md` near the top if they are not there, and
  keep the rest exactly.
- **GEMINI.md** (Gemini CLI, Antigravity): if missing and the project uses those tools (or the human wants all
  agents covered), write `assets/GEMINI.md`. If present, add its pointer line.
- Other agents' rule files (`.cursor/rules`, `.github/copilot-instructions.md`): leave them; add one line
  "Follow AGENTS.md." if they contradict it.

## 5. The `.shipshape/` folder and git hooks

- Write `.shipshape/config` from `assets/shipshape/config` and fill in `code_paths`, `check_commands`,
  `default_branch` and `live_commands` from the survey.
- Copy `assets/shipshape/context.sh`, `context.ps1`, `docs-gate.sh` and `gitignore` (as `.shipshape/.gitignore`).
- Copy `assets/githooks/commit-msg`, `pre-commit` and `pre-push` into `.githooks/`. If the project already has
  hooks there, merge the logic (call theirs first). Then:
  ```
  git config core.hooksPath .githooks
  ```
  Tell the human that every clone needs this one command (it is also printed by the session report), because
  git does not copy hook settings.
- Append `assets/gitattributes` to `.gitattributes` (create it if missing): hook scripts must keep LF line
  endings, or `sh` fails on Windows checkouts.
- Make the scripts executable (`git update-index --chmod=+x .githooks/* .shipshape/*.sh`).

## 6. CI and PR template

- Pick `assets/ci/python.yml`, `node.yml` or `generic.yml`, keep only the steps whose commands exist in the
  project, append the job in `assets/ci/docs-gate-job.yml`, and write it as `.github/workflows/ci.yml`. If a CI
  workflow exists, add only the `docs-gate` job to it.
- Write `assets/pull_request_template.md` as `.github/pull_request_template.md` if none exists.

## 7. Verify, commit, PR

1. Run the check commands; test the hooks once (a code-only commit must be rejected, then accepted with the
   docs; a commit on the default branch must be refused).
2. Commit with STATUS/CHANGELOG/DECISIONS updated (`D-00N Adopted shipshape: …`).
3. Push and open the PR with the walkthrough (`../shipshape/references/land.md`). Note that branch protection
   needs the human (or `gh api`, where the plan allows it; GitHub Free can't protect private personal repos).

## New project (empty folder or no commits yet)

1. Ask four questions (unattended: choose the defaults shown and record them as assumptions):
   stack/language (default: the one the request implies), public or private (private), solo or team (solo),
   will it run live for real users (no).
2. `git init -b main`, a stack-appropriate `.gitignore`, a minimal runnable skeleton with one real test.
3. Steps 3-6 above (the docs describe the skeleton; DECISIONS starts with `D-001 Project set up with shipshape`
   plus the stack choice and why).
4. First commit **on main** (the only commit ever made on main directly), then `git config core.hooksPath
   .githooks`.
5. With the human's OK: `gh repo create <name> --private --source . --push` (or public), then protect `main`
   where the plan allows it.
6. Continue the user's actual request on a feature branch, with the `shipshape` workflow.

## Never

- Overwrite or reorder an existing CLAUDE.md, AGENTS.md, README or doc. Merge.
- Commit secrets or `.env` files; put names of env vars in the docs, never values.
- Change runtime behaviour, dependencies or settings in the adopt PR.
- Push to the default branch (except the first commit of a new project).
