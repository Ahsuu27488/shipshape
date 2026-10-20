# Writing the plan

A plan is cheap insurance: five minutes of writing saves an afternoon of building the wrong thing. Keep it
short. If you can describe the whole diff in one sentence, the task is T0 and needs no plan.

## Before writing it

- Explore narrowly: the files you will change, their callers, their tests, the decisions that touch them.
  If your tool can run a separate research agent for a wide search, use it, so the main conversation stays
  focused.
- Find the existing pattern for this kind of change in the codebase and follow it. Do not invent a second way.

## What the plan contains

```
Goal:          one sentence, in the user's words
Tier:          T1 / T2, and why
Files:         the files that will change (and new files)
Out of scope:  what this change deliberately does NOT do
Approach:      3-7 numbered steps, each small enough to commit alone
The check:     the exact command(s) or observation that will prove it works
               (a test name, a build, a request and its expected answer, a screenshot)
Risks:         what could break, and who would notice
Rollback:      how to undo it (T2: the exact commands)
Assumptions:   anything you had to decide without asking (unattended mode)
```

## Where it goes

- **T1:** in chat. Then carry on.
- **T2:** `docs/plans/<yyyy-mm-dd>-<slug>.md`, committed on the branch. Then stop and wait for the human's
  explicit approval. "Looks good" counts; silence does not.
- **Unattended (any tier):** always the file, committed first, because nobody is watching the chat.

## After approval

Work the steps in order. If reality forces a different approach, update the plan file (T2) or say so in chat
(T1) before continuing. The plan should match what was built.
