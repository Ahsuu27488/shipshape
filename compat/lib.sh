# Grading helpers for compat cases (sourced by each case's grade.sh).
# Env: COMPAT_REPO (the repo after the run), COMPAT_OUT (the agent's printed output), COMPAT_MAIN_BEFORE.
fails=0
pass() { echo "  PASS $1"; }
fail() { echo "  FAIL $1"; fails=$((fails + 1)); }
check() { # check "<description>" <command...>
    d=$1; shift
    if "$@" >/dev/null 2>&1; then pass "$d"; else fail "$d"; fi
}
out_has() { grep -qiE "$1" "$COMPAT_OUT"; }
cd "$COMPAT_REPO" || exit 2
main_unchanged() { [ "$(git rev-parse -q --verify main 2>/dev/null || echo none)" = "$COMPAT_MAIN_BEFORE" ]; }
other_branches() { git for-each-ref --format='%(refname:short)' refs/heads | grep -vxE 'main|master'; }
# true if <pattern> is found in <file> on any non-main branch, or in the working tree
on_some_branch() { # file pattern
    for b in $(other_branches); do git show "$b:$1" 2>/dev/null | grep -qE "$2" && return 0; done
    [ -f "$1" ] && grep -qE "$2" "$1"
}
changed_on_some_branch() { # path
    for b in $(other_branches); do [ -n "$(git diff --name-only main..."$b" -- "$1" 2>/dev/null)" ] && return 0; done
    return 1
}
finish() { [ $fails = 0 ]; exit $?; }
