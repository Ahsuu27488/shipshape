#!/bin/sh
# shipshape-run: give any coding agent a task, walk away, and come back to a pull request and a report.
#
#   tools/shipshape-run.sh [options] "<task>"
#     --agent NAME      claude (default) | codex | gemini | agy | cursor | copilot
#     --budget-min N    wall-time budget for the agent, in minutes (default 60)
#     --base BRANCH     branch to start from (default: default_branch in .shipshape/config, else main)
#     --model MODEL     model for the agent (default: the agent's own default)
#     --no-pr           don't push or open a PR (local run; the compat tests use this)
#     --keep            keep the worktree after opening the PR
#     --dry-run         print what would run, run nothing
#
# What it does: makes a fresh worktree on branch auto/<date>-<slug>, runs the agent headless there with the
# shipshape-unattended skill and SHIPSHAPE_UNATTENDED=1, enforces the time budget, then re-runs the project's
# check_commands ITSELF (the agent never grades its own work), pushes, and opens a draft PR (ready only when
# every check passed and the agent reported success) whose body is the agent's report plus the wrapper's
# check results. The report is also copied to .shipshape/last-report.md so the next session summarises it.
# Optional: SHIPSHAPE_NOTIFY="<command>" runs after the PR exists, with SHIPSHAPE_PR_URL and SHIPSHAPE_RESULT set.
# SHIPSHAPE_MAX_USD caps a Claude run's cost (default 5).

set -u
agent=claude; budget=60; base=""; model=""; open_pr=1; keep=0; dry=0; task=""
while [ $# -gt 0 ]; do
    case "$1" in
        --agent) agent=$2; shift 2 ;;
        --budget-min) budget=$2; shift 2 ;;
        --base) base=$2; shift 2 ;;
        --model) model=$2; shift 2 ;;
        --no-pr) open_pr=0; shift ;;
        --keep) keep=1; shift ;;
        --dry-run) dry=1; shift ;;
        -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
        *) task="$task${task:+ }$1"; shift ;;
    esac
done
[ -n "$task" ] || { echo "shipshape-run: give a task, e.g. tools/shipshape-run.sh --agent codex \"add a /health endpoint\"" >&2; exit 2; }

repo=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "shipshape-run: run it inside a git repository." >&2; exit 2; }
cd "$repo" || exit 2
cfg() { [ -f "$1/.shipshape/config" ] && sed -n "s/^$2=//p" "$1/.shipshape/config" | tail -n 1 | tr -d '\r'; }
[ -n "$base" ] || base=$(cfg "$repo" default_branch)
[ -n "$base" ] || base=main

slug=$(printf '%s' "$task" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\{1,\}/-/g; s/^-//; s/-$//' | cut -c1-40 | sed 's/-$//')
[ -n "$slug" ] || slug=task
stamp=$(date +%Y%m%d-%H%M)
branch="auto/$(date +%Y%m%d)-$slug"
git rev-parse --verify -q "refs/heads/$branch" >/dev/null && branch="$branch-$(date +%H%M%S)"
wt="$(dirname "$repo")/$(basename "$repo").shipshape/$stamp-$slug"
runs="$repo/.shipshape/runs/$stamp-$slug"

remote=""
git remote get-url origin >/dev/null 2>&1 && remote=origin
start="$base"
if [ -n "$remote" ]; then
    git fetch -q origin "$base" 2>/dev/null && start="origin/$base"
fi

prompt="Use the shipshape-unattended skill for this task. You are already on branch $branch in an isolated worktree made for this run: do not create or switch branches, do not push and do not open a pull request (the wrapper does that); finish by writing your report to .shipshape/last-report.md. Task: $task"

case "$agent" in
    claude)  set -- claude -p "$prompt" --permission-mode auto --permission-prompts none --max-budget-usd "${SHIPSHAPE_MAX_USD:-5}" ${model:+--model "$model"} ;;
    codex)   set -- codex exec --sandbox workspace-write -c approval_policy=never --skip-git-repo-check ${model:+-m "$model"} "$prompt" ;;
    gemini)  set -- gemini --approval-mode auto_edit ${model:+-m "$model"} -p "$prompt" ;;
    agy)     set -- agy -p "$prompt" --mode accept-edits ${model:+--model "$model"} ;;
    cursor)  bin=cursor-agent; command -v cursor-agent >/dev/null 2>&1 || bin=agent
             set -- "$bin" -p --force ${model:+--model "$model"} "$prompt" ;;
    copilot) set -- copilot -p "$prompt" --allow-tool write --allow-tool shell ${model:+--model "$model"} ;;
    custom)  set -- sh -c "${SHIPSHAPE_AGENT_CMD:?set SHIPSHAPE_AGENT_CMD for --agent custom}" shipshape-agent "$prompt" ;;
    *) echo "shipshape-run: unknown agent '$agent'" >&2; exit 2 ;;
esac

# Extra flags for the agent, e.g. Antigravity's headless mode denies shell commands without allow rules:
#   SHIPSHAPE_AGENT_ARGS="--dangerously-skip-permissions"   (only in a disposable clone or VM)
# shellcheck disable=SC2086
[ -n "${SHIPSHAPE_AGENT_ARGS:-}" ] && set -- "$@" $SHIPSHAPE_AGENT_ARGS

if [ "$dry" = 1 ]; then
    echo "worktree: $wt (branch $branch from $start)"
    printf 'agent:   '; printf '%s ' "$@"; echo
    echo "checks:  $(cfg "$repo" check_commands)"
    exit 0
fi
command -v "$1" >/dev/null 2>&1 || { echo "shipshape-run: '$1' is not installed or not on PATH." >&2; exit 2; }

mkdir -p "$runs" "$(dirname "$wt")"
git worktree add -q -b "$branch" "$wt" "$start" || { echo "shipshape-run: could not create the worktree." >&2; exit 1; }
echo "shipshape-run: $agent working on '$task'"
echo "  branch $branch, worktree $wt, budget ${budget} min, log $runs/agent.log"

cd "$wt" || exit 1
export SHIPSHAPE_UNATTENDED=1 SHIPSHAPE_RUN=1
began=$(date +%s)
if command -v timeout >/dev/null 2>&1; then
    timeout "$((budget * 60))" "$@" </dev/null >"$runs/agent.log" 2>&1
else
    "$@" </dev/null >"$runs/agent.log" 2>&1
fi
agent_exit=$?
minutes=$(( ($(date +%s) - began + 59) / 60 ))
[ "$agent_exit" = 124 ] && echo "  the agent hit the ${budget}-minute budget"
if grep -qi 'auto-denied\|cannot prompt\|permission.*denied' "$runs/agent.log" 2>/dev/null; then
    echo "  note: the agent was denied tool permissions in headless mode. Add allow rules for git and your check"
    echo "  commands in its settings (Antigravity: permissions.allow), or set SHIPSHAPE_AGENT_ARGS in a disposable clone."
fi

# Work left uncommitted is committed as WIP so nothing is lost (the PR will be a draft).
if [ -n "$(git status --porcelain -- . ':(exclude).shipshape/last-report.md' 2>/dev/null)" ]; then
    git add -A -- . ':(exclude).shipshape/last-report.md' ':(exclude).shipshape/runs' 2>/dev/null
    git commit -q -m "wip: unattended run ended with uncommitted work [no-docs]" 2>/dev/null || true
fi

# The wrapper's own verification.
checks=$(cfg "$wt" check_commands)
checks_ok=0
if [ -n "$checks" ]; then
    sh -c "$checks" >"$runs/checks.log" 2>&1 && checks_ok=1
    check_line="\`$checks\` → $( [ $checks_ok = 1 ] && echo passed || echo FAILED )"
else
    check_line="no check_commands in .shipshape/config: nothing verified independently"
fi

ahead=$(git rev-list --count "$start..HEAD" 2>/dev/null || echo 0)
report="$runs/report.md"
if [ -f .shipshape/last-report.md ]; then
    cp .shipshape/last-report.md "$report"
else
    { echo "# ⛔ Stopped: the agent left no report"
      echo ""; echo "The agent ($agent) exited with code $agent_exit and wrote no .shipshape/last-report.md."
      echo "Last lines of its output:"; echo '```'; tail -n 30 "$runs/agent.log"; echo '```'; } >"$report"
fi
{
    echo ""
    echo "## Independent checks (shipshape-run)"
    echo "- $check_line"
    echo "- Agent: $agent, exit code $agent_exit, ${minutes} min of a ${budget}-min budget, $ahead commit(s) on \`$branch\`"
    if [ -f "$runs/checks.log" ] && [ $checks_ok = 0 ]; then
        echo ""; echo '```'; tail -n 25 "$runs/checks.log"; echo '```'
    fi
} >>"$report"
cp "$report" "$repo/.shipshape/last-report.md" 2>/dev/null

result=stopped
head -n 1 "$report" | grep -q '✅' && [ $checks_ok = 1 ] && result=done
pr_url=""
if [ "$ahead" = 0 ]; then
    echo "  the agent made no commits; nothing to push."
elif [ "$open_pr" = 1 ] && [ -n "$remote" ]; then
    if git push -q -u origin "$branch" 2>"$runs/push.log"; then
        title="[shipshape] $(printf '%s' "$task" | cut -c1-60)"
        draft="--draft"; [ "$result" = done ] && draft=""
        pr_url=$(gh pr create --base "$base" --head "$branch" --title "$title" --body-file "$report" $draft 2>>"$runs/push.log") \
            || echo "  could not open the PR (see $runs/push.log); the branch is pushed."
    else
        echo "  push failed (see $runs/push.log); the work is on $branch locally."
    fi
fi

cd "$repo" || exit 1
if [ -n "$pr_url" ] && [ "$keep" = 0 ]; then git worktree remove --force "$wt" 2>/dev/null; fi

echo ""
echo "shipshape-run: $(head -n 1 "$report" | sed 's/^# //')"
echo "  checks: $check_line"
[ -n "$pr_url" ] && echo "  PR: $pr_url"
echo "  report: $repo/.shipshape/last-report.md"
if [ -n "${SHIPSHAPE_NOTIFY:-}" ]; then
    SHIPSHAPE_PR_URL="$pr_url" SHIPSHAPE_RESULT="$result" sh -c "$SHIPSHAPE_NOTIFY" || true
fi
[ "$result" = done ] && exit 0 || exit 1
