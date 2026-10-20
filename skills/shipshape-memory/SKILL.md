---
name: shipshape-memory
description: Creates and maintains a project's memory docs (docs/STATUS.md, DECISIONS.md, ARCHITECTURE.md, CHANGELOG.md) from the real code, so every future session in any coding agent knows where the project stands, what was decided and why, and how the code connects. Use when a change is finished and before its final commit, when the session report says the docs are stale, when the user says "checkpoint", "save progress", "update the docs" or "remember this", and to build the docs for the first time in an existing project.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
---

# shipshape-memory: the project's memory

Every agent session starts with no memory of the last one. These four files are the memory. They must describe
**reality, verified**, not intentions. A doc claim you did not check is worse than no claim, because the next
session will trust it.

| File | What it holds | Size |
|---|---|---|
| `docs/STATUS.md` | Current truth only: what works (verified), what is in progress, known gaps, **Next**, live state | Short. Loaded every session |
| `docs/DECISIONS.md` | Numbered decisions `D-001`, `D-002`…: what was decided, **why**, where it lives in the code. Never renumbered or deleted; an old one is marked `*(superseded by D-0NN)*` | Grows slowly. Loaded every session |
| `docs/ARCHITECTURE.md` | The map of the code **as built**: modules and what each owns, data model, interfaces (endpoints, CLI, events), how a request or job flows, commands to run/test/build | Kept exact. Loaded every session |
| `docs/CHANGELOG.md` | History, newest first: date, commit, what changed, root causes of fixes | Grows. Read on demand |

If the project already has its own memory skill or docs layout (for example a `/checkpoint` skill, or docs in
another folder), use theirs and stop here.

## Mode A: build the memory for the first time (existing code, no docs)

Research the project the way a new senior engineer would in their first week, then write what you found.
**Everything must come from the code, the git history and commands you ran, never from guesses.**

1. **Survey.** List the tree (top two levels), read the README, the package manifest(s) (`package.json`,
   `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`…), CI config, Dockerfile/scripts, and any
   existing agent files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules`, `.github/copilot-instructions.md`).
2. **Find the entry points** (main, server start, CLI, app router, workers) and follow one real request or job
   end to end through the code. That path is the spine of ARCHITECTURE.md.
3. **Find the data:** models, schemas, migrations, files it reads/writes, external services and their config
   (names of env vars only, **never values**).
4. **Run the checks** the project has (tests, type check, lint, build) and record the real result
   ("41 tests, 2 failing: …"). If they can't run, say why.
5. **Read the history:** `git log --oneline -50`, plus `git log --stat` for the biggest changes. Recover
   decisions that are clearly visible (a commit "switch from X to Y because Z", a comment explaining a rule).
   Record them as decisions with their evidence ("from commit abc1234"). Do not invent reasons you can't see:
   write "reason not recorded" instead.
6. **Write the four files** from `../shipshape-adopt/assets/docs/` templates:
   - ARCHITECTURE: the runtime picture, a module table (path → responsibility), the data model, interfaces,
     the request/job flow, commands. Name real files and functions only; spot-check each one exists.
   - STATUS: last updated + commit, what works (only verified items), known gaps (from failing tests, TODOs,
     issues), **Next** (from the user, the README roadmap, open TODOs; ask if unclear).
   - DECISIONS: `D-001 Project memory set up with shipshape` plus the recovered decisions.
   - CHANGELOG: one entry for today ("Memory docs created") and, optionally, a summary of earlier history.
7. **Show the human a 5-line summary** of what the docs now say, and ask them to correct anything wrong. Their
   corrections are the most valuable lines in the docs.

## Mode B: checkpoint (keep it current, after every change)

1. **What changed since the docs were last true?**
   ```
   git log -1 --format=%H -- docs/STATUS.md          # last time STATUS was committed
   git log --oneline <that>..HEAD                       # commits since
   git diff --stat <that>                               # committed + uncommitted since
   git status --short
   ```
   Read the actual diffs of code files, not only the commit messages.
2. **Verify before recording.** Run the checks (`check_commands` in `.shipshape/config`, or the commands in
   ARCHITECTURE.md). Record the real counts. Only list something under "What works" if it was exercised this
   session or a passing test covers it; otherwise mark it untested.
3. **Edit, don't rewrite:**

| Doc | When | What to change |
|---|---|---|
| STATUS.md | **always** | "Last updated" date + commit, what works, in progress, known gaps (remove fixed, add found), Next |
| CHANGELOG.md | **always** | New entry on top: date, commit (or "uncommitted"), what changed, root cause for fixes |
| DECISIONS.md | a choice was made, a rule changed, or a lesson was learned the hard way | Append the next `D-NNN`: **Decision. Why. Where it lives.** If it replaces an older one, add `*(superseded by D-NNN)*` to the old heading. Never renumber or delete |
| ARCHITECTURE.md | modules, files, data/schema, interfaces, commands, flows or important constants changed | Fix the affected tables and lists so they match the code exactly |

4. **Consistency check:** every known gap still true (grep to confirm)? Every path and name in ARCHITECTURE.md
   still exists (spot-check with search)? Does STATUS "Next" still make sense?
5. **Stage the docs with the code they describe**, in the same commit. The repo's `commit-msg` hook rejects code
   commits without STATUS.md and CHANGELOG.md (bypass `[no-docs]` only for changes with no behaviour change).
6. Tell the human in 2-3 lines what the docs now say changed.

## Rules for good memory

- **Current truth in STATUS, history in CHANGELOG.** Move old detail out of STATUS so it stays short: it is
  loaded into every session.
- **Every decision has a why.** "We use cents" is half a decision; "integers in cents, because float rounding
  made totals off by a cent (D-002)" is a decision.
- **Settings are not facts.** If a value is a setting the user can change, write "the X setting (N today)",
  never "the N-minute rule".
- **No secrets, ever.** Names of env vars and files, never their values.
- **Dates are absolute** (2026-10-20), never "yesterday" or "last week".
- **Plain words.** The human reads these too.
