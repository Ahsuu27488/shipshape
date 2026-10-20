. "$(dirname "$0")/../../lib.sh"
check "typo fixed on a branch" on_some_branch README.md 'Customers receive a receipt'
check "main unchanged (no commit on main)" main_unchanged
check "no plan file for a typo" sh -c '! ls docs/plans/2*.md 2>/dev/null | grep -q . && ! git log --all --name-only --format= | grep -q "^docs/plans/2"'
finish
