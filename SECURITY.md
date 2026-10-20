# Security policy

## Reporting a vulnerability

Please report security issues privately through
[GitHub's private vulnerability reporting](https://github.com/Ahsuu27488/shipshape/security/advisories/new),
not in a public issue. Include the shipshape version, your agent and operating system, and steps to reproduce.
You can expect a first response within a week.

## Security model

- **Instructions are not enforcement.** The skills tell agents what not to do (merge, touch live systems, open
  secrets). The enforcement is in places an agent cannot talk its way past: the repository's git hooks
  (`.githooks/`), CI, branch protection where your plan allows it, and, in Claude Code, the plugin's PreToolUse
  hooks. For unattended runs, the strongest guard is the environment: run in a worktree or clone with no
  production credentials, and give the agent a GitHub token limited to that repository's contents and pull
  requests.
- **No network access of its own.** The scripts use `sh`, `git`, `sed` and `grep` only.
- **Secrets.** The `pre-commit` hook refuses `.env`/key files and lines that look like common credentials
  (cloud keys, GitHub/Slack/OpenAI/Anthropic/Google tokens, private keys) and never prints the matched value.
  It is a safety net, not a scanner you can rely on.
- **Hook fail-safe.** If a guard script cannot parse its input, it gives no opinion and the agent's normal
  permission rules apply; it never blocks or allows on its own error.

## In scope

- A guard that allows what it documents as asked or denied (for example a commit on `main` passing silently with
  `git_guard=ask`).
- A hook or script that leaks a secret value into output, logs or a report.
- `shipshape-run` pushing to, merging into or force-pushing the default branch.
- Anything in the skills that leads an agent to run destructive or live actions without the documented steps.
