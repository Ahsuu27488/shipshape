# Changing a live system safely

A **live system** is anything real people or real money depend on right now: a production server or database,
a deployed site, a bot that posts, a scheduled job, a phone app in users' hands, a payment flow. Any change that
touches one is **T2**: plan file, the human's go-ahead, and the steps below. Unattended mode never performs any
step of this file. It writes the plan and stops.

## Before

1. **What is in flight?** Jobs running, uploads half done, users mid-checkout, queued messages. A restart in the
   middle can lose or duplicate them. Wait for a quiet moment, or drain the queue first.
2. **What mode is it in?** Live vs dry run vs paused. Say it to the human. Never change the mode silently.
3. **Backup:** the data you might damage (database copy, export, snapshot), and confirm the backup is readable.
4. **The smallest safe test first:** a dry run, a staging copy, a feature flag that is off, one account instead
   of all, a canary. Watch it work there before the real thing.
5. **Write the rollback before you need it:** the exact commands that undo this change (previous build, previous
   migration, flag off, restore from backup). If there is no rollback, say so and get explicit approval.
6. **Builds must not take the running version down.** Build into a new place and switch only when the build has
   finished; never delete the live build before the new one exists.

## During

- One change at a time. Keep a log of what you ran and when.
- If anything surprises you, stop, put things back, and report. Do not improvise on production.

## After

- Watch it: logs, health checks, error rates, the next real job, for a set time (say 10-30 minutes, or until
  the next real event).
- Report with evidence: what you watched and what it showed.
- Put back anything you changed for testing (routes, caps, flags, modes).
- Record it in STATUS.md (what is live now) and, if a lesson was learned, DECISIONS.md.

## Hard rules

- Never touch production credentials, payment details or real users' data beyond what the task needs.
- Never run an experiment on the live system that could be run on a copy.
- A "small fix" to a live system is still T2.
- Every attempt that has a real-world effect (a post, an email, a charge, a rate-limited call) counts. Keep
  them rare and deliberate.
