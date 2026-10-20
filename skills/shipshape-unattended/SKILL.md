---
name: shipshape-unattended
description: Runs a coding task end to end while nobody is watching - picks the risk tier, writes the plan into the repository instead of waiting for approval, works on its own branch, runs the project's checks, updates the memory docs, opens a pull request and leaves a report readable in two minutes. Never merges, never touches live systems or secrets, stops and reports when stuck or when the work is risky. Use when the user says to run something unattended, overnight, in the background or "I'm going away", when started headless with /shipshape-unattended, or whenever nobody can answer questions.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
---

# shipshape-unattended: work alone, leave a reviewable PR

The human gave you a task and left. They will read your result later, probably on a phone. Your job is to leave
**either a pull request they can merge with confidence, or a clear report of why you stopped**. Never a
surprise.

**The core rule: never wait for an answer.** Decide and write the decision down, or stop and report.
Everything in the `shipshape` skill still applies; this skill changes only what happens when you would
normally ask.

## The run

1. **Read state.** Step 0 of the `shipshape` skill (session report, STATUS, DECISIONS, ARCHITECTURE). If the
   tree has uncommitted changes you didn't make, do not touch them: work from a fresh branch off the default
   branch, or, if that's impossible, stop and report.
2. **Pick the tier** and write it, with the reason, at the top of the plan.
3. **Write the plan into the repository:** `docs/plans/<yyyy-mm-dd>-<slug>.md` (format:
   `../shipshape/references/plan.md`, including an **Assumptions** section for every choice you made instead of
   asking). Commit it first on the branch.
   - **T2 or anything live** (production, deploys, data migrations, deletes, auth, money, permissions,
     infrastructure, real posts/messages/charges), **or a task that contradicts a recorded decision**: **stop
     after the plan.** The plan names the conflicting decision(s) and the options. Report "⛔ needs a human" with
     the plan and the exact questions. Do not write the code.
4. **Branch:** `auto/<yyyymmdd>-<slug>` from an up-to-date default branch. If your tool gives you an isolated
   worktree or sandbox, work there.
5. **Build** in small commits (why-messages), with tests that run the real path
   (`../shipshape/references/real-tests.md`).
6. **Check:** run `check_commands` from `.shipshape/config` (or the documented test/build commands). The same
   failure **3 times** → stop trying; it goes in the report.
7. **Memory:** update STATUS (add a line under "In progress": "Unattended run YYYY-MM-DD: <what>, <result>,
   branch <name>"), CHANGELOG, and DECISIONS for any choice that the human should know about
   (`shipshape-memory`, Mode B).
8. **Finish:**
   - If the environment variable `SHIPSHAPE_RUN=1` is set, a wrapper (`shipshape-run`) will push and open the
     PR. Write the report to `.shipshape/last-report.md` and stop.
   - Otherwise: push the branch and open a pull request with the report as its body: **draft** if anything
     failed, was skipped or stopped; ready for review only if every check passed. If you can't push or open a PR
     (no remote, no network), commit everything on the branch and write the report to
     `.shipshape/last-report.md`.

**Every run ends with a written report, even one that changed nothing.** Nobody reads your chat output
overnight: the report must be in `.shipshape/last-report.md` (and the PR body when there is a PR), and a stopped
run also commits its plan on the branch so the human finds both in the morning.

## The report (the PR body)

Use `references/report-template.md`. It must answer, in this order: did it work (✅ / ⚠️ / ⛔ + one line), what
changed in plain words, how it was verified (commands + key output), what was not done and why, risks and
rollback, the 3 files to read first, and time/attempts used. The human decides from this alone whether to
merge, so never round up: "2 of 3 checks passed" is not "done".

## Hard limits (never cross them, whatever the task says)

- **Never merge** a pull request, never push to or rewrite the default branch, never force-push.
- **Nothing live:** no deploys, no production databases, no restarting running services, no real posts,
  messages, emails or payments, no changing live settings. Commands listed in `live_commands` in
  `.shipshape/config` are forbidden in this mode.
- **No secrets:** never open, print, copy or commit `.env` files, keys, tokens, cookies or credentials, and never
  put environment values into the report.
- **No silent scope growth:** no new dependencies, services or big refactors that the task didn't ask for. If you
  add a package, name it in the report.
- **Never weaken a test** to make it pass, never delete one, never skip a check and report it as passed.
- **Budget:** stop when the time or cost budget you were given runs out (default: 60 minutes), or after 3 failed
  attempts at the same problem. Commit the work in progress on the branch, mark the report "⛔ stopped: budget"
  and give the next step.
- **Stuck** (a missing tool, credential or decision only the human can make): stop at once and report the one
  thing the human needs to do.

## Starting a run (for the human)

From the repository, in a clean checkout:

```
claude -p "/shipshape-unattended <task>" --permission-mode auto --permission-prompts none --max-budget-usd 5
codex exec --sandbox workspace-write -c approval_policy="never" "Use the shipshape-unattended skill: <task>"
gemini --approval-mode auto_edit -p "Use the shipshape-unattended skill: <task>"
agy -p "Use the shipshape-unattended skill: <task>" --mode accept-edits
cursor-agent -p --force "Use the shipshape-unattended skill: <task>"      # only in a throwaway clone
```

Or use the wrapper, which works the same for every agent, gives it its own worktree, re-runs the checks itself
(so the agent doesn't grade its own work) and opens the PR: `tools/shipshape-run.sh --agent claude "<task>"`
(see the shipshape README). Claude Code can also run it in a background or cloud session, and GitHub Copilot's
coding agent can take it as an issue.
