# Debugging: find the cause before the fix

Use this for a bug, a failing test (yours, the suite's or CI's), a crash, or anything that behaves in a way you
didn't expect. A fix made before you know the cause is a guess: it tends to hide the symptom, add a second bug,
or move the first one somewhere harder to see. Finding the cause first feels slower and is almost always faster.

For a request to fix a bug, start in Step 1 of the shipshape skill: read, look at the history and trace (steps 1,
3 and 4 here) before the plan, so the plan names the likely cause and its check. Anything that edits code, even a
reproduction test or debug prints, follows the tier: at T2 it waits for the approved plan (unattended: stop there).

## The steps

1. **Read the whole error.** The message, every line of the stack trace, the file names and line numbers, and
   the warnings printed before it. It often names the cause outright.
2. **Make it happen on purpose.** Find the exact steps that trigger it every time, best of all as a test that
   fails because of the bug: that test later proves the fix (`real-tests.md`). If it won't happen reliably,
   collect more evidence (logs, inputs, timing) instead of guessing. Never experiment on a live system to make
   it happen: use a copy (`live-safety.md`).
3. **Look at what changed.** `git log` and `git diff` since the last version that worked, plus new dependencies,
   config and environment. When a good version exists, `git bisect` finds the commit that broke it.
4. **Find where it first goes wrong, not where it shows.** Follow the bad value backwards: what passed it in,
   and what passed it to that, until you reach its source. Across several parts (CI → build → deploy, request →
   service → database), print what enters and leaves each part, run it once, and see where good data turns bad.
   Run it on a copy or as a dry run, never as a live deploy or a real post (`live-safety.md`).
   Put it next to similar code that works and note each difference, including the ones you're sure are harmless.
5. **Test one hypothesis at a time.** Say it in one sentence, with your evidence: "X happens because Y; I can
   tell from Z." Make the smallest change that proves or disproves it. Wrong? Undo that change and form a new
   hypothesis; never stack a second change on a failed one. If you don't understand something, say so and find out.
6. **Fix the cause.** A failing test first (if step 2 didn't give you one, write it now). Where no test can reach
   it (a CI setting, a paid API, a phone), a check that fails before and passes after, done by hand and written
   down (`real-tests.md`). Then one change at the source (no "while I'm here" extras), then the whole suite.
   Put the root cause in the commit message and the CHANGELOG entry.
7. **Three failed fixes: stop.** After 3 fixes that didn't work, or when each fix makes the problem appear
   somewhere new, the design is the likely problem, not the details. Tell the human what you tried and what each
   attempt showed, and decide together before a fourth. Unattended: stop and report (`shipshape-unattended`).

## When no cause turns up

If it really comes from outside your code (a flaky network, a third-party outage, timing you can't control),
write down what you checked, handle it in code (a retry, a timeout, a clear error) and add logging so the next
occurrence leaves evidence. Most "no cause" verdicts are an investigation that stopped too early.

## Stop signs

You are guessing, not debugging, if you catch yourself at one of these. Go back to step 2.

- "Let me just try…" before you can say what the cause is.
- Several changes at once, "to save time".
- A fix you never saw fail first, in a test or a written check.
- Making the failing test pass by weakening, skipping or deleting it (never: `real-tests.md`).

Adapted from the `systematic-debugging` skill of superpowers (github.com/obra/superpowers, MIT, © Jesse Vincent).
