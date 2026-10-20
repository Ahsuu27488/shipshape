<!-- shipshape:start (managed by shipshape; edit outside the markers) -->
## How to work in this repository (shipshape)

**Before writing any code, in every session:**
1. Run `sh .shipshape/context.sh` (Windows without sh: `pwsh -File .shipshape/context.ps1`) and act on its warnings.
2. Read `docs/STATUS.md` (where we are, what's next), `docs/DECISIONS.md` (what was decided and why; never undo a
   decision without a new entry) and `docs/ARCHITECTURE.md` (how the code connects).
3. Read the code you will change and its callers. Never build on a guess; if the docs and the code disagree, the
   code is the truth and the docs get fixed.
4. If a request contradicts a decision in DECISIONS.md, stop before editing: quote the decision and its reason, and
   ask the user to confirm. A confirmed change gets a new decision that supersedes the old one.

**Every change:** say the tier (T0 trivial / T1 normal / T2 risky: data, auth, money, deletes, live systems),
work on a branch (never commit to the default branch), name the check that proves it works, test the real code
path, read the whole diff, then update `docs/STATUS.md` + `docs/CHANGELOG.md` (and DECISIONS / ARCHITECTURE when
relevant) in the same commit. The `commit-msg` hook rejects code commits without them; `[no-docs]` is only for
changes with no behaviour change. Land through a pull request with What / Why / How verified / Risk.

**T2 and anything live:** written plan in `docs/plans/`, the human's go-ahead, dry run first, written rollback.
**Unattended:** never merge, never touch anything live or any secret; stop and report when stuck.

If the shipshape skills are installed, use them (`shipshape`, `shipshape-memory`, `shipshape-unattended`).
Project-specific rules below and in the docs take precedence over these defaults.
<!-- shipshape:end -->

## This repository

shipshape is itself a set of agent-neutral skills (`skills/`), a Claude Code plugin layer (`.claude-plugin/`,
`hooks/`, `scripts/`, `agents/`), an unattended wrapper (`tools/`), and tests (`tests/` unit, `evals/` Claude evals,
`compat/` cross-agent runs). Rules specific to this repo:

- Skills must stay agent-neutral: no vendor tool names, plain verbs (`tests/test_skills.py` enforces it).
- Shell scripts are POSIX `sh` with LF endings and must never fail the agent on their own errors.
- Edit eval fixtures only in `tests/fixtures/tinyshop.sh`, then run `python tools/sync_eval_fixtures.py`.
- Bump the version in `.claude-plugin/plugin.json` and every SKILL.md `metadata.version` together.
- Publishing (tags, releases, directory submission) is a live action: only when Ahsan says so.
