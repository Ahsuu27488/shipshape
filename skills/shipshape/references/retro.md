# When something broke: a short, blameless retro

Use this after a bug reached users, a live run failed, or a "passing" change turned out broken.

1. **Stabilise first.** Roll back or switch off (see `live-safety.md`). The retro comes after.
2. **Timeline:** what happened, when, who or what noticed, from logs and git history. Facts only.
3. **Root cause:** ask "why" until you reach something you can change. "The code had a bug" is not a root cause;
   "the test used a fake that never ran the real upload function" is.
4. **Why didn't our checks catch it?** Which test, review step, CI job or doc should have, and why it didn't.
5. **Fix forever, not once:**
   - a regression test that runs the real path and fails without the fix;
   - a `D-NNN` entry in DECISIONS.md: what happened, the lesson, the rule from now on;
   - if it should never recur: a guard (a check in CI, a hook, an assertion) rather than a sentence.
6. **Record:** CHANGELOG (the fix and the root cause), STATUS (known gaps updated).

No blame. The question is always "what in our process let this through", never "who did it".
