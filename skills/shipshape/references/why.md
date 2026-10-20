# Why cards

Short reasons for each habit, shown to the human just in time (see "Teaching" in SKILL.md). Each card has an
id (the heading). Show it inline in at most 6 lines, in your own words. Stories marked **(real)** happened in a real project built with AI coding agents
(kept anonymous); never present the others as real events, say "for example" instead.

## memory
- **Doing:** reading STATUS, DECISIONS and ARCHITECTURE before touching code.
- **Why:** an agent starts every session with no memory. Without the docs it re-decides settled questions and
  breaks things that were fixed on purpose.
- **Without it (for example):** a project lost a week re-adding a check that a decision had removed for a good reason; the
  reason was only in an old chat.
- **Pros / you:** big teams keep design docs and decision records. You keep four short Markdown files.

## understand-first
- **Doing:** reading the code you'll change and its callers before editing, and saying where the project stands.
- **Why:** code built on a guess about how things connect is the most expensive kind of bug: it looks right.
- **Without it (for example):** a change to a "helper" broke three callers nobody had looked at.
- **Pros / you:** engineers read before they write. You: the 3-6 line orientation before the first edit.

## tiers
- **Doing:** rating the change T0 / T1 / T2.
- **Why:** process should match risk. A typo doesn't need a design doc; a database migration does.
- **Without it (for example):** either everything is slow, or the risky change gets the typo treatment.
- **Pros / you:** strong teams scale review to risk. You: one line, "Tier: T1 because…".

## branches
- **Doing:** working on a branch, never on main.
- **Why:** main should always work. A branch is a free undo button and a place for review.
- **Without it (for example):** a half-finished change on main is what gets deployed, or what the next session builds on.
- **Pros / you:** at large companies, nothing lands on main without review. You: `git switch -c feat/…`.

## plan-first
- **Doing:** writing a short plan, with the check that proves it works, before coding.
- **Why:** it's cheap to fix a plan and expensive to fix code. Naming the check first stops "it looks done".
- **Without it (for example):** an afternoon spent building the wrong thing, then an evening undoing it.
- **Pros / you:** design docs for big changes. You: 10 lines in chat, or a file for risky work.

## small-changes
- **Doing:** small commits and small PRs that each leave the code working.
- **Why:** small changes are easy to review, easy to revert and easy to understand later.
- **Without it (for example):** one giant change breaks something, and nobody can find which part.
- **Pros / you:** reviewers at big companies reject huge changes. You: one idea per commit.

## real-tests
- **Doing:** testing the real function, not only a fake of it.
- **Why:** a fake only proves the fake works.
- **Without it (real):** every test passed with a fake uploader; the real one crashed right before the final click,
  three times, live.
- **Pros / you:** integration tests beside unit tests. You: at least one test through the real path.

## read-the-diff
- **Doing:** reading the whole diff before committing.
- **Why:** it's the last moment a mistake is cheap. Agents also touch things you didn't ask for.
- **Without it (for example):** a debug print with a token in it reached the repository.
- **Pros / you:** every change at big companies is read by a second person. You: read it once, slowly.

## fresh-eyes
- **Doing:** a separate reviewer (agent, session or person) checking a risky change.
- **Why:** the author sees what they meant, not what they wrote.
- **Without it (real):** a "deleted" route quietly deleted the 29 jobs that pointed at it, and the history with them.
- **Pros / you:** mandatory code review. You: a reviewer agent, or a second pass with the checklist.

## pull-requests
- **Doing:** opening a PR, even on a solo project.
- **Why:** one place for the diff, the reason, the evidence and CI, and an easy undo (revert the merge).
- **Without it (for example):** months later nobody knows why a change was made.
- **Pros / you:** every change is a reviewed PR. You: a short PR body, then merge it yourself.

## ci
- **Doing:** tests, types and lint run automatically on every push.
- **Why:** humans and agents forget to run checks. A machine doesn't.
- **Without it (for example):** a change that "worked on my machine" broke the build for a day.
- **Pros / you:** CI gates every merge. You: one workflow file from shipshape.

## decision-log
- **Doing:** writing a numbered decision (D-NNN) when you choose something or learn a lesson.
- **Why:** the "why" is the first thing lost, and the next person (or agent) undoes it.
- **Without it (for example):** a deliberate rule was "fixed" back to the bug it prevented.
- **Pros / you:** architecture decision records. You: four lines in DECISIONS.md, never deleted, only superseded.

## dry-run-rollback
- **Doing:** testing on a copy or dry run first, and writing the undo before a live change.
- **Why:** production is the worst place to discover a mistake, and a panic is the worst time to invent a fix.
- **Without it (real):** a failed build deleted the running site's files and took the public site down.
- **Pros / you:** staging, canaries, feature flags. You: dry run first, rollback commands in the plan.

## unattended
- **Doing:** working alone on a branch, writing decisions down, stopping instead of guessing at risky steps.
- **Why:** an agent left alone should leave a reviewable PR, not a surprise.
- **Without it (for example):** an overnight run "fixed" a test by deleting it, and the report said everything passed.
- **Pros / you:** bots open PRs; humans merge. You: read the morning report, then merge or not.
