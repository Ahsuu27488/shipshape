# Reviewing a diff

Read the whole diff (`git diff <base>...HEAD`, plus `git status` for new untracked files) as if someone else
wrote it. You are looking for things that make the change **wrong**, not for things you would have written
differently.

## Report only these

1. **Correctness:** wrong logic, off-by-one, wrong condition, unhandled None/null/empty, wrong units
   (seconds vs ms, cents vs currency), timezone mistakes, wrong error handling (swallowed errors, retries that
   repeat a non-idempotent action).
2. **Requirements:** something the plan or request asked for is missing, or something not asked for was added.
3. **Breakage elsewhere:** callers, other modules, config, migrations, public APIs or data formats this change
   affects but did not update. Search for every caller of a changed function.
4. **Tests:** the changed behaviour has no test that runs the real path (`real-tests.md`); a test was weakened.
5. **Safety:** secrets in code or logs, injection (SQL, shell, HTML), destructive operations without a guard,
   anything that touches a live system without the live-safety steps.
6. **Memory:** code changed but STATUS/CHANGELOG did not; a decision was made but not recorded; ARCHITECTURE
   now names a file or function that no longer exists.

## For each finding

`file:line`, one sentence on what is wrong, the concrete scenario that breaks it, and your confidence
(high / medium / low). Fix high-confidence correctness findings before landing. List the rest for the human.

## Don't

- Report style, naming or formatting preferences, or "consider adding" ideas, unless they cause a bug.
- Pad the review. "No correctness issues found" is a valid result.
