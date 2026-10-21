#!/bin/sh
# Run every compat case (or the ones named) for one agent, and append the results to compat/results/<agent>.log.
#   sh compat/run-all.sh <agent> [case ...]
here=$(cd "$(dirname "$0")" && pwd)
agent=${1:?usage: run-all.sh <agent> [case ...]}
shift
[ $# -gt 0 ] || set -- $(ls "$here/cases")
mkdir -p "$here/results"
log="$here/results/$agent.log"
echo "### $(date '+%Y-%m-%d %H:%M') $agent" >> "$log"
for c in "$@"; do
    snap=$(mktemp); cp "$here/run-case.sh" "$snap"; SNAP_HERE="$here" sh "$snap" "$agent" "$c" --keep 2>&1 | tee -a "$log" | grep -E '^(RESULT|  FAIL)'
done
