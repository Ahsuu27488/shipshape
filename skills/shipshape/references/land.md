# Landing a change: commits, push, pull request, CI

## Commits

- Small and working: each commit builds and passes the tests.
- Message: a short summary line (imperative, under ~70 characters), a blank line, then **why** the change was
  needed and anything surprising. The diff already says what.
- Stage files by name. Never `git add -A` blindly: it sweeps in secrets, build output and other people's work.
- Docs (STATUS/CHANGELOG, etc.) go in the same commit as the code they describe. For a commit with no
  behaviour change, put `[no-docs]` in the message so the docs gate lets it through.
- Never `--no-verify` to get past a hook. A hook that rejects you is telling you something; fix that.

## Push and pull request

1. `git push -u origin <branch>`.
2. Open a PR (`gh pr create`, or the link git prints). Body:

```
## What
<plain words, 1-3 lines>

## Why
<the problem or request; link the issue / plan file / decision>

## How it was verified
<commands run and their key output; screenshots for UI>

## Risk and rollback
<what could break; how to undo it>

## Review guide
<the 2-3 files to read first>
```

3. Wait for CI. If it fails, read the log, fix the cause, push again. Never merge red.
4. Merge when CI is green **and** the human agrees. On a solo project the human may merge their own PR after
   reading the diff; that is still review, done by the person who owns the code. Prefer squash merge for
   small PRs so the default branch reads as one line per change.
5. After merge: delete the branch, `git switch main && git pull`.

## No remote, or no `gh`

- No remote yet: commit on the branch, then tell the human how to add one (`gh repo create` or the hosting
  site's "new repository" page). Merge locally with `git switch main && git merge --no-ff <branch>` only
  when the human says so.
- No `gh`: push, then give the human the compare URL the push printed.

## Branch protection

Where the hosting plan allows it, protect the default branch (require a PR and green CI):
`gh api -X PUT repos/<owner>/<repo>/branches/main/protection` with the required checks. GitHub Free does not
allow protection rules on private personal repositories; there the repo's `.githooks/pre-push` is the guard.
