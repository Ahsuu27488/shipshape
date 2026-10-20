#!/bin/sh
# shipshape PreToolUse guard for Bash commands (Claude Code).
# Interactive sessions: asks before commits/pushes on main/master (git_guard setting), destructive commands and
# the project's live commands. Unattended runs (SHIPSHAPE_UNATTENDED=1): denies them, plus any merge.
# Prints nothing (= no opinion) for everything else. Never fails the tool call on its own errors.

input=$(cat)
cmd=$(printf '%s' "$input" | tr '\n' ' ' | sed -nE 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/p' | head -n 1)
[ -n "$cmd" ] || exit 0
lc=$(printf '%s' "$cmd" | tr '[:upper:]' '[:lower:]')

guard="${CLAUDE_PLUGIN_OPTION_GIT_GUARD:-ask}"
unattended="${SHIPSHAPE_UNATTENDED:-0}"
dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$dir" 2>/dev/null || exit 0

decide() {
    # $1 = ask|deny, $2 = reason (no double quotes or backslashes)
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
    exit 0
}
risky() {
    # Interactive: ask. Unattended: deny.
    if [ "$unattended" = "1" ]; then decide deny "shipshape (unattended): $1 Not allowed in an unattended run; stop and put it in the report."; fi
    decide ask "shipshape: $1"
}
has() { printf '%s' "$lc" | grep -qE "$1"; }

config=""
root=$(git rev-parse --show-toplevel 2>/dev/null) && [ -f "$root/.shipshape/config" ] && config="$root/.shipshape/config"
cfg() { [ -n "$config" ] && sed -n "s/^$1=//p" "$config" | tail -n 1 | tr -d '\r'; }
default=$(cfg default_branch); [ -n "$default" ] || default=main
branch=$(git branch --show-current 2>/dev/null)
on_default=0
if git rev-parse --verify -q HEAD >/dev/null 2>&1; then
    case "$branch" in "$default"|main|master) on_default=1 ;; esac
fi

git_cmd='(^|[;&|(][[:space:]]*|[[:space:]])git([[:space:]]+-c[[:space:]]+[^[:space:]]+|[[:space:]]+-C[[:space:]]+[^[:space:]]+)*[[:space:]]+'

# Merging a pull request
if has 'gh[[:space:]]+pr[[:space:]]+merge'; then
    risky "merging a pull request. The human merges after reading the PR."
fi

# Force-push or push straight to the default branch
if has "${git_cmd}push" ; then
    if has '(^|[[:space:]])(-f|--force|--force-with-lease)([[:space:]=]|$)' ; then
        if [ "$on_default" = "1" ] || has "[[:space:]:/](main|master|$default)([[:space:]]|$)"; then
            decide deny "shipshape: force-pushing the default branch rewrites shared history. Never do this; open a PR instead."
        fi
        risky "force-push rewrites the branch history on the remote."
    fi
    # explicit default-branch refspec, or a bare "git push [origin]" while on the default branch
    if has "push[^;&|]*[[:space:]:](main|master|$default)([[:space:];&|]|$)"        || { [ "$on_default" = "1" ] && has 'push([[:space:]]+-[a-z-]+)*([[:space:]]+[a-z0-9_.-]+)?[[:space:]]*($|[;&|])'; }; then
        [ "$guard" = "off" ] && [ "$unattended" != "1" ] && exit 0
        [ "$guard" = "block" ] || [ "$unattended" = "1" ] && decide deny "shipshape: pushing to the default branch. Push a feature branch and open a pull request."
        decide ask "shipshape: this pushes to the default branch ($default). Professional flow: push a feature branch and open a PR. Allow anyway?"
    fi
fi

# Committing on the default branch
if has "${git_cmd}commit([[:space:]]|$)" && [ "$on_default" = "1" ]; then
    if [ "$unattended" = "1" ] || [ "$guard" = "block" ]; then
        decide deny "shipshape: no commits on $branch. Create a branch first: git switch -c feat/short-name"
    fi
    [ "$guard" = "off" ] || decide ask "shipshape: you are on $branch. Commit here anyway? (Professional flow: git switch -c feat/short-name, then commit.)"
fi

# Destructive commands (removing build output and caches is fine)
safe_rm='(^|[;&|[:space:]])rm[[:space:]]+-[a-z]+([[:space:]]+(\./)?(node_modules|dist|build|out|target|coverage|\.next|\.cache|__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)/?)+[[:space:]]*($|[;&|])'
if has "$safe_rm"; then :
elif has '(^|[;&|[:space:]])rm[[:space:]]+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r|-r[[:space:]]+-f|-f[[:space:]]+-r|--recursive)' \
   || has "${git_cmd}(reset[[:space:]]+--hard|clean[[:space:]]+-[a-z]*f|stash[[:space:]]+(drop|clear)|checkout[[:space:]]+--[[:space:]]|restore[[:space:]]+--source)" \
   || has "${git_cmd}push[^;&|]*--delete" \
   || has '(drop[[:space:]]+(table|database|schema)|truncate[[:space:]]+table|delete[[:space:]]+from[[:space:]]+[a-z_."]+[[:space:]]*(;|$))'; then
    risky "this command deletes or overwrites work or data. Is there a backup or a way to undo it?"
fi

# The project's own live commands
live=$(cfg live_commands)
if [ -n "$live" ] && printf '%s' "$cmd" | grep -qE "$live"; then
    risky "this command touches a live system (live_commands in .shipshape/config). Follow live-safety: in-flight work, dry run, rollback."
fi
exit 0
