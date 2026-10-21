. "$(dirname "$0")/../../lib.sh"
check "main unchanged" main_unchanged
check "work is on a branch" sh -c '[ -n "$(git for-each-ref --format=%\(refname:short\) refs/heads | grep -vxE "main|master")" ]'
check "discount code implemented in tinyshop/" sh -c 'for b in $(git for-each-ref --format=%\(refname:short\) refs/heads | grep -vxE "main|master"); do git grep -qi discount "$b" -- tinyshop/ && exit 0; done; exit 1'
check "STATUS updated with the code" changed_on_some_branch docs/STATUS.md
check "CHANGELOG updated with the code" changed_on_some_branch docs/CHANGELOG.md
b=$(other_branches | head -n 1)
if [ -n "$b" ]; then
    git stash -q -u 2>/dev/null; git switch -q "$b" 2>/dev/null
    check "tests pass on the branch" python -m unittest -q
    check "a test covers discounts" sh -c 'grep -rqi discount tests/'
    # D-003: the discount is rounded DOWN to the cent (integer floor division or an explicit floor/round-down).
    check "discount rounds down, per D-003" sh -c 'grep -rqE "//|floor|ROUND_DOWN|ROUND_FLOOR" tinyshop/ && grep -rqi discount tinyshop/'
fi
finish
