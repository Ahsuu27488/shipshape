# Tests that exercise the real code path

**The rule:** for every behaviour you change, at least one test runs the **real** function (the one the
program calls in production) with realistic input, not only a fake or mock of it.

## Why this rule exists

In one real project, every test of the upload step used a fake uploader. All of them passed. The real upload
function had a variable named `deadline` that clashed with a new parameter of the same name, and it crashed
right before the final click, three times in a row, live. The fake never ran that code. A second time, a new
helper was fully unit-tested while the loop that called it still used a variable the change had removed; every
live poller crashed for twelve minutes. Both times the tests were green and the product was broken.

## Checklist

- [ ] Does a test call the real function or endpoint (not only its fake)?
- [ ] Do fakes stand in only for what is slow, paid, external or dangerous (network, payments, third-party
      APIs, real posting), and nothing else?
- [ ] Does the test go through the same entry point production uses (the loop, the handler, the CLI), at least
      once per changed path?
- [ ] **Bug fix:** is there a test that failed before the fix and passes after? Run it both ways.
- [ ] Are the inputs realistic (real-shaped data, edge values: empty, zero, very large, unicode, None/null)?
- [ ] Did you run the whole suite, not only the new test, and read the result?

## Never

- Weaken, skip or delete a failing test to make the suite pass. Fix the code, or explain to the human why
  the test is wrong and get agreement.
- Mock the function under test.
- Claim a test passes without running it in this session.

## When the real path can't run in tests

(It talks to a paid API, a phone, a live account.) Then: test everything up to the boundary with the real
code, keep the fake as thin as possible, and add a manual verification step to the plan and the PR
("verified once against the real service: …"). Say plainly what was not tested.
