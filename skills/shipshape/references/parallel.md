# Several tasks at once

Professional teams split work so that two people never edit the same files at the same time. With agents the
rule is the same.

1. **Split by files, not by idea.** Each piece must be doable without another piece's result and must touch
   files no other piece touches. If two pieces need the same file, they are one piece, or they run one after
   the other.
2. **One isolated checkout per piece:** `git worktree add ../<repo>-<slug> -b <branch>` (or your tool's own
   worktree / background-session feature). Never two writers in one folder.
3. **One branch and one PR per piece.** Small PRs get reviewed; a giant combined PR gets skimmed.
4. **Memory docs are shared files:** each piece adds its own CHANGELOG entry and its own STATUS line; whoever
   merges second resolves the doc conflict by keeping both.
5. **Check the combination.** After the pieces merge, run the full test suite on the default branch once more.
6. **Clean up:** `git worktree remove ../<repo>-<slug>` after merging.
