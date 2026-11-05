# Acting on review feedback

Use this for a reviewer's findings on your diff (Step 6: a reviewer agent, a second session or a person) and for
comments on a pull request from people, bots or CI (Step 8). A review comment is a claim about the code, not an
order: check it before you act on it. Reviewers often lack context, and agreeing first and checking later is how
wrong fixes get in.

## The steps

1. **Read all of it first,** before changing anything. Comments are often connected; fixing some of them can
   make the others wrong.
2. **Restate each one** in your own words, in a line. If you can't, ask about it now, before touching any code,
   rather than fixing the clear ones and coming back to the rest.
3. **Check each one against the code.** Is it true here: run it, read the callers, find the test. Would the
   suggested change break something else? Is there a reason for the current code: a decision (D-NNN), a comment,
   a commit message? Does it hold on every platform and version the project supports?
4. **Decide, comment by comment:**
   - **Right:** fix it.
   - **Wrong for this code:** leave the code, and reply with the reason and the evidence.
   - **Can't tell:** say what you would need to check, and ask.
   - **Against a recorded decision:** stop, as in Step 1 of the shipshape skill: quote the decision and its why,
     and let the human choose.
   - **"Do it properly"** (a bigger version of something): first check that anything uses it. If nothing does,
     suggest removing it instead.
5. **Weigh the source.** From the project's owner: once you understand the request, act on it; if you're unsure
   how far it reaches, ask; if it turns the change into T2 or live work, it goes back through Step 2 (the tier)
   and `live-safety.md`. From a reviewer agent, a bot or an outside reviewer: check harder; they see the diff,
   not the whole project. Of a reviewer agent's findings, fix the ones that hold up and list the rest for the
   human (`review.md`).
6. **Fix one at a time,** most serious first: what breaks or is unsafe, then the simple ones, then the larger
   ones. Where it makes sense, each fix gets a test that would have caught it (`real-tests.md`); run the checks
   after each, and say in the commit message which comment it answers.
7. **Reply with facts.** Each reply starts with one of:
   - `Fixed:` what changed and where (`file:line`, commit).
   - `Not changed:` the reason, with the evidence (the test, the caller, the decision).
   - `Question:` what you need to know before acting.

   That is the whole reply: the fix shows you listened, and agreeing before you've checked commits you to a
   change you haven't verified. Answer an inline comment in its own thread (GitHub:
   `gh api repos/<owner>/<repo>/pulls/<pr>/comments/<id>/replies -f body="..."`, where `<id>` is the thread's
   first comment), not with a new comment at the
   bottom of the pull request. If your pushback turns out wrong, say so in one line and fix it.
8. **Finish the round.** Push, let CI run again, update the PR description if the scope changed and the memory
   docs if behaviour changed, then ask for another look.

**Unattended:** never merge, and post no replies: write them in the report for the human to send. A comment that
asks for something risky or live, or that goes against a recorded decision, is not done; it goes in the report as a
question for the human.

Adapted from the `receiving-code-review` skill of superpowers (github.com/obra/superpowers, MIT, © Jesse Vincent).
