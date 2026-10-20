#!/bin/sh
# Cross-agent compatibility run: one case, one agent, a fresh fixture repo, graded on what ended up in the repo.
#   sh compat/run-case.sh <agent> <case> [--keep]
#   agents: claude | codex | agy | gemini | cursor | copilot
# The shipshape skills are installed the way a user would: into the repo's .agents/skills/ (read by Codex,
# Cursor, Copilot, Gemini CLI, Antigravity) - or, for Claude Code, loaded as the plugin (--plugin-dir).
# Runs happen in a throwaway folder with the agent's approvals turned off; never point this at a real repo.
# Prints one line per check and "RESULT <agent> <case> PASS|FAIL"; exit 0 on PASS.

set -u
agent=${1:?usage: run-case.sh <agent> <case> [--keep]}
case_name=${2:?usage: run-case.sh <agent> <case> [--keep]}
keep=${3:-}
here=${SNAP_HERE:-$(cd "$(dirname "$0")" && pwd)}
root=$(cd "$here/.." && pwd)
case_dir="$here/cases/$case_name"
[ -d "$case_dir" ] || { echo "no such case: $case_name" >&2; exit 2; }

work=$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/ss-compat-$$")
mkdir -p "$work"
repo="$work/repo"
mode=$(cat "$case_dir/mode" | tr -d '\r\n')
sh "$root/tests/fixtures/tinyshop.sh" "$repo" "$mode" "$root" >/dev/null 2>&1 || { echo "fixture failed" >&2; exit 2; }
cd "$repo" || exit 2
[ -d .git ] || git init -q -b main
git config user.name "Compat Runner"
git config user.email "compat@example.com"
if [ "$agent" != claude ]; then
    mkdir -p .agents/skills
    cp -R "$root/skills/." .agents/skills/
fi
# The installed skills are the user's tooling, not project content.
printf '.agents/\n' >> .git/info/exclude 2>/dev/null
main_before=$(git rev-parse -q --verify main 2>/dev/null || echo none)
printf '%s\n' "$main_before" > "$work/main-before"

prompt=$(cat "$case_dir/prompt.txt")
[ -f "$case_dir/unattended" ] && export SHIPSHAPE_UNATTENDED=1
out="$work/agent-output.txt"
limit=${COMPAT_TIMEOUT_SECONDS:-1200}
case "$agent" in
    claude)  set -- claude -p "$prompt" --plugin-dir "$root" --permission-mode bypassPermissions --model "${COMPAT_CLAUDE_MODEL:-claude-sonnet-5-5}" ;;
    codex)   set -- codex exec --sandbox workspace-write -c approval_policy=never --skip-git-repo-check "$prompt" ;;
    agy)     set -- agy -p "$prompt" --model "${COMPAT_AGY_MODEL:-gemini-3.8-flash-high}" --mode accept-edits --dangerously-skip-permissions ;;
    gemini)  set -- gemini --approval-mode yolo -p "$prompt" ;;
    cursor)  bin=cursor-agent; command -v cursor-agent >/dev/null 2>&1 || bin=agent; set -- "$bin" -p --force "$prompt" ;;
    copilot) set -- copilot -p "$prompt" --allow-all-tools ;;
    *) echo "unknown agent $agent" >&2; exit 2 ;;
esac
command -v "$1" >/dev/null 2>&1 || { echo "RESULT $agent $case_name SKIP (not installed)"; exit 3; }
started=$(date +%s)
if command -v timeout >/dev/null 2>&1; then timeout "$limit" "$@" </dev/null >"$out" 2>&1; else "$@" </dev/null >"$out" 2>&1; fi
code=$?
secs=$(( $(date +%s) - started ))

echo "== $agent / $case_name (exit $code, ${secs}s, work dir $work)"
COMPAT_REPO="$repo" COMPAT_OUT="$out" COMPAT_MAIN_BEFORE="$main_before" sh "$case_dir/grade.sh"
graded=$?
if [ $graded = 0 ]; then verdict=PASS; else verdict=FAIL; fi
echo "RESULT $agent $case_name $verdict ${secs}s"
[ "$keep" = "--keep" ] || [ $graded != 0 ] || rm -rf "$work"
[ $graded = 0 ]
