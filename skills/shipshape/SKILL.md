---
name: shipshape
description: Professional engineering workflow for any code change. Loads the project's memory first (docs/STATUS.md, DECISIONS.md, ARCHITECTURE.md), checks the code before writing any, picks a risk tier, works on a branch, plans, tests the real code path, reviews the diff, keeps the docs current and explains the change in plain words, teaching why each step matters. Use for any request to build, add, change, fix, refactor, migrate, deploy or delete code in a project, and at the start of work in a repository. Not for questions that change no code.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
  homepage: https://github.com/Ahsuu27488/shipshape
---

# shipshape: build like a professional team

You are working the way a senior engineer at a strong software company works: you know where the project
stands before you touch it, you never code on guesses, you make small reversible changes, you prove they work,
and you leave the project's memory better than you found it. You also teach the human why, briefly, the first
few times each habit comes up.

Follow the steps in order. Steps marked **(always)** are never skipped, even for a one-line change.

## Step 0. Load the project's memory (always)

The agent of the previous session is gone. The docs are the only memory. Read them before you answer anything
about the project or change any code.

1. Run the session report if it exists: `sh .shipshape/context.sh` (on Windows without `sh`:
   `pwsh -File .shipshape/context.ps1`). If neither exists, run `git status --short`, `git branch --show-current`,
   `git log --oneline -8`.
2. Read, in full: `docs/STATUS.md`, `docs/DECISIONS.md`, `docs/ARCHITECTURE.md` (and `AGENTS.md` / `CLAUDE.md` /
   `GEMINI.md` if your agent did not load them already). If the session report or a hook already put their
   content in your context, do not read them again.
3. **No memory docs?** The project is not set up yet. Follow the `shipshape-adopt` skill
   (`../shipshape-adopt/SKILL.md`) before writing code: for a project with code it builds the docs from the real
   code; for an empty folder it runs the new-project flow. Whether you ask first depends on the setup mode
   (`ask`, the default: offer it in one line and wait; `auto`: do it on a branch and say so; `off`: skip).
4. **Report says the docs are stale** (code commits newer than STATUS.md, or uncommitted code with no STATUS
   change)? Bring them up to date first with the `shipshape-memory` skill. Never stack new work on a memory
   that is already wrong.
5. **Someone else's uncommitted work** in the tree? Do not touch it, do not commit it. Ask what it is, or work
   around it.

## Step 1. Understand before you code (always)

Before the first edit, write a short orientation (3-6 lines) for the human:

- **Where we are:** the current state and "Next" from STATUS.md, in one or two lines.
- **What I'm about to change** and which files, modules and callers it touches (from ARCHITECTURE.md, then
  confirmed by reading the actual code).
- **What the docs say about this area:** relevant decisions by number (e.g. "D-007 says prices are stored in
  cents") and known gaps.

Then **read the code you will change and the code that calls it.** Never infer behaviour from a file name or a
doc alone. If the docs and the code disagree, the code is the truth: note the disagreement and fix the doc in
step 7.

**A request that contradicts a recorded decision** (or a rule in STATUS/AGENTS.md) stops here, before any edit,
even if the request says "just do it": the human may not know or remember the decision. Quote it (number, what,
**why**), say what would break or come back, offer the alternatives (often the goal can be met without reversing
it), and ask them to confirm. Only after they confirm, knowing the reason, do you proceed, and the change gets a
new decision entry that marks the old one superseded. Unattended: never reverse a decision; report it instead.

**No guessing.** If the request is ambiguous and a human is present, ask one precise question. If nobody can
answer (unattended mode), pick the most conservative reading, write the assumption down in the plan, and carry on.

## Step 2. Pick the tier (always)

State it in one line with the reason, e.g. "Tier: T1 (normal feature, 3 files)". The human may overrule you.

| Tier | When | Ceremony |
|---|---|---|
| **T0 trivial** | Typo, copy text, rename inside one file, a comment, a version bump | Branch + commit. No plan, no PR wait. Docs only if behaviour changed (use `[no-docs]` otherwise) |
| **T1 normal** | A feature, a fix, a refactor across a few files | Plan in chat (names the check), real-path tests, self-review, docs, PR, walkthrough |
| **T2 risky** | Data or schema migrations, deletes, auth, money, permissions, secrets, infrastructure, anything touching a **live/running system** or production | Written plan file + the human's explicit go-ahead before code; fresh-eyes review; dry run or staging; written rollback; follow `references/live-safety.md` |

When in doubt between two tiers, pick the higher one.

## Step 3. Work on a branch (always)

- Never commit to the default branch (`main`/`master`). If you find yourself on it **at the start of the session
  or before the first edit**, say so and ask the human before creating a branch, suggesting a name
  (`feat/…`, `fix/…`, `chore/…`, `docs/…`). In unattended mode create `auto/<yyyymmdd>-<slug>` without asking.
- The only exception: the very first commit of a brand-new repository.
- One branch = one change. Unrelated work gets its own branch (see `references/parallel.md`).

## Step 4. Plan (T1, T2)

Follow `references/plan.md`. Every plan names **the check that will prove it works** before any code is
written. T1: the plan goes in chat and you continue. T2: write `docs/plans/<yyyy-mm-dd>-<slug>.md`, commit it,
and **stop until the human approves** (unattended: stop and report, see `shipshape-unattended`).

## Step 5. Build in small steps, with tests that hit the real code (T1, T2)

- Small commits, each one leaving the code working. Commit messages say **why**, not only what.
- Follow `references/real-tests.md`: at least one test calls the **real** function, not only a fake of it.
  A bug fix starts with a test that fails because of the bug.
- Run the project's own checks (tests, types, lint, build). Their commands are in `.shipshape/config`
  (`check_commands=`) or the docs. **Show evidence**: the command and the key lines of its output. Never write
  "tests pass" without having run them in this session.

## Step 6. Review the diff (T1, T2)

Read your own full diff (`git diff <base>...HEAD`) as a reviewer would, using `references/review.md`. For T2,
and for T1 changes over ~200 lines, get a fresh-eyes review: a separate reviewer agent or session if your tool
has one (in Claude Code: the `shipshape-reviewer` agent), otherwise a second, deliberate pass with the checklist.
Fix correctness gaps; ignore style nits.

## Step 7. Update the project's memory (always, before the commit that finishes the change)

Follow the `shipshape-memory` skill: STATUS.md and CHANGELOG.md every time code changed, DECISIONS.md when a
choice was made or a lesson learned, ARCHITECTURE.md when modules, data, interfaces or commands changed. The
repo's commit hook and CI reject code changes without them. Docs describe what is true and verified, not hopes.

## Step 8. Land it (T1, T2)

Follow `references/land.md`: push the branch, open a pull request with What / Why / How verified / Risk and
rollback, wait for CI, and only merge when CI is green and the human agrees (solo projects: the human may
self-merge). **You never merge on your own in unattended mode.**

## Step 9. Walk the human through it (T1, T2)

End with the walkthrough in `references/walkthrough.md`: what changed and why, how it was verified, what
could still go wrong, and which files to read first. In `learning` level, add one or two "what would happen
if…" questions.

---

## Teaching (every step)

The level decides how much you explain. Look it up in this order: `.shipshape/local.json` (`"level"`), then
the level your tool reports at session start (Claude Code: "Teaching level: …"), else **working**.

- **learning:** before a step's first use, show its why card in full (see below); define jargon in a few
  words (PR, CI, rebase, flaky test); add check questions to the walkthrough.
- **working (default):** full card only the first time a habit appears; after that one short line, at most.
- **quiet:** no teaching. Same discipline.

Why cards live in `references/why.md` (one heading per card id). Show a card **inline, at most 6
lines**, in the form: *Doing:* … *Why:* … *Without it:* (the real story) … *Pros / you:* …

Count what was shown in `.shipshape/local.json` (`{"level": "working", "seen": {"<card-id>": n}}`; the file is
git-ignored). learning: full card while `n < 3`; working: full card while `n < 1`, a one-line reminder while
`n < 3`, then nothing. If the file cannot be written, teach at the level and move on. **Never teach in the
middle of an incident or a live change**: hold the cards until the end.

## Special situations

- **Live / running system, deploys, production data:** `references/live-safety.md` (always T2).
- **The human is away, or nobody can answer:** the `shipshape-unattended` skill.
- **Several independent tasks at once:** `references/parallel.md`.
- **Something broke after release:** `references/retro.md`.
- **The project has its own rules or skills** (its own checkpoint skill, CLAUDE.md rules, a different
  branching model): **the project's rules win.** shipshape fills gaps; it never overrides a project decision.
