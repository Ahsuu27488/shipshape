# Decision Log

> Each entry: what was decided, **why**, and where it lives. Numbering is permanent: never renumber or delete;
> supersede with a new entry and mark the old heading *(superseded by D-NNN)*. The full original plan, with the
> research behind these choices, is `docs/PLAN.md`.

**D-001 One agent-neutral source, three layers.** (2026-10-20)
Layer 1 is the skills in the open Agent Skills format (`skills/`), read natively by 40+ agents. Layer 2 is what
`shipshape-adopt` writes into a user's repo (memory docs, AGENTS.md block, git hooks, CI): it enforces the rules for
every agent and human. Layer 3 is per-agent extras, today the Claude Code plugin (hooks, reviewer agent, settings).
Nothing important may exist only in Layer 3.
*Why:* Ahsan wants it to work for everyone's coding agent, not only Claude; hook formats differ per agent, but git
hooks and CI are shared by all. *Where:* `skills/`, `skills/shipshape-adopt/assets/`, `.claude-plugin/`, `hooks/`.

**D-002 Few deep skills, all prefixed `shipshape`.** (2026-10-20)
Six skills (`shipshape` router, `-memory`, `-adopt`, `-unattended`, `-checkup`, `-explain`); detail lives in
`references/`, loaded on demand. *Why:* outside Claude Code, skill folders share one global namespace
(`.agents/skills/`), so generic names would collide; fewer skills trigger more reliably and cost less context.
*Where:* `skills/*/SKILL.md`; enforced by `tests/test_skills.py`.

**D-003 Ceremony scales with risk (T0 / T1 / T2).** (2026-10-20)
T0 trivial = branch + commit; T1 normal = plan naming its check, real-path tests, review, docs, PR, walkthrough;
T2 risky (data, auth, money, deletes, live systems) = plan file + the human's go-ahead + fresh-eyes review + dry run +
rollback. *Why:* the main complaint about workflow plugins is the same heavy process for every change.
*Where:* `skills/shipshape/SKILL.md`.

**D-004 Project memory is the strongest part, modelled on Relay.** (2026-10-20)
STATUS (current truth), DECISIONS (numbered, superseded never deleted), ARCHITECTURE (map as built), CHANGELOG
(history); built from the real code on first adoption; loaded at every session start (Claude: SessionStart hook +
CLAUDE.md imports; others: AGENTS.md block + router step 0); a commit-msg hook and a CI job reject code changes
without STATUS + CHANGELOG (`[no-docs]` bypass). *Why:* Ahsan's main pain is agents forgetting earlier sessions,
misreading how code connects, and coding on guesses; his Relay setup solved it in one repo. *Where:*
`skills/shipshape-memory/`, `skills/shipshape-adopt/assets/`, `scripts/session-start.sh`.

**D-005 Memory setup: `ask` by default, `auto` available.** (2026-10-20)
The Claude plugin's `auto_setup` setting (`ask` / `auto` / `off`). A "no" is remembered per folder in the plugin's
data folder. Home folders and drive roots are never touched. *Why:* Ahsan wants new projects set up without asking
(he sets `auto`); the public default must not create files unasked. *Where:* `scripts/session-start.sh`,
`.claude-plugin/plugin.json`.

**D-006 The main-branch guard asks at session start, not only at commit.** (2026-10-20)
`git_guard` (`ask` default / `block` / `off`): the session report tells the agent it is on main and to ask for a branch
before the first change; the PreToolUse hook asks (or denies) on commit/push. The repo's own `pre-commit`/`pre-push`
hooks always refuse (override `SHIPSHAPE_ALLOW_MAIN=1`). *Why:* Ahsan's request; catching it before the edits is
cheaper than at commit time. *Where:* `.shipshape/context.sh`, `scripts/guard-bash.sh`, `githooks/`.

**D-007 Unattended runs are verified by the wrapper, not the agent.** (2026-10-20)
`tools/shipshape-run.sh` makes the worktree, runs any agent headless, then re-runs `check_commands` itself and only
opens a ready PR if they pass and the agent reported success; otherwise a draft. It never merges. T2 work stops at
the plan. *Why:* an agent grading its own work is the failure mode unattended mode must avoid; one tool for all
agents also serves as the compat runner's model. *Where:* `tools/shipshape-run.sh`, `skills/shipshape-unattended/`.

**D-008 Claude evals can't authenticate from the desktop app on this PC; compat runs carry the behaviour gate.** (2026-10-20)
`claude plugin eval` child sessions reported "Not logged in" (they don't inherit the desktop app's host sign-in), and
`~/.claude/settings.json` sets `ANTHROPIC_MODEL` to a non-Claude model. The release gate therefore uses
`compat/run-case.sh`, which drives real `claude -p --plugin-dir . --model claude-sonnet-5-5` sessions (and other
agents' CLIs) against the fixture and grades the repo state. The `evals/` suite stays for CI (an
`ANTHROPIC_API_KEY` secret) or a `claude setup-token` login. *Where:* `compat/`, `evals/`, `CLAUDE.md`.

**D-009 Why-card stories are labelled real or example.** (2026-10-20)
Cards marked **(real)** describe incidents from Relay (anonymised: the fake uploader D-055, the route-delete cascade
D-063, the failed build D-092); the rest say "for example". *Why:* teaching with invented incidents presented as real
would be dishonest. *Where:* `skills/shipshape/references/why.md`.
