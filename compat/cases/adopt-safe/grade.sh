. "$(dirname "$0")/../../lib.sh"
check "kept the existing CLAUDE.md house rule" on_some_branch CLAUDE.md 'keep every module under 200 lines'
check "AGENTS.md has the shipshape block" on_some_branch AGENTS.md 'shipshape:start'
check "STATUS.md exists" on_some_branch docs/STATUS.md 'Next'
check "ARCHITECTURE built from the real code" on_some_branch docs/ARCHITECTURE.md 'tinyshop/(cart|payments)\.py'
check "DECISIONS has D-001" on_some_branch docs/DECISIONS.md 'D-001'
check "commit-msg hook installed" sh -c 'for b in $(git for-each-ref --format=%\(refname:short\) refs/heads); do git cat-file -e "$b:.githooks/commit-msg" 2>/dev/null && exit 0; done; [ -f .githooks/commit-msg ]'
check "main unchanged" main_unchanged
finish
