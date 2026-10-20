#!/bin/sh
# shipshape SessionStart hook (Claude Code). Everything printed goes into the new session's context:
# the settings, the project's live state, its memory docs, and what to do when a project has no memory yet.
# Must stay fast and must never fail the session start.

dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$dir" 2>/dev/null || exit 0
here="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
teaching="${CLAUDE_PLUGIN_OPTION_TEACHING:-working}"
guard="${CLAUDE_PLUGIN_OPTION_GIT_GUARD:-ask}"
setup="${CLAUDE_PLUGIN_OPTION_AUTO_SETUP:-ask}"
data="${CLAUDE_PLUGIN_DATA:-$HOME/.shipshape}"
declined="$data/declined-setup.txt"

echo "# shipshape"
echo ""
echo "Teaching level: $teaching (a repo can override it in .shipshape/local.json). Commits on main/master: $guard. Memory setup: $setup."
if [ "${SHIPSHAPE_UNATTENDED:-0}" = "1" ]; then
    echo "UNATTENDED RUN: nobody can answer questions. Follow the shipshape-unattended skill: plan into the repo, own branch, never merge, nothing live, no secrets, stop and report when stuck."
fi
echo ""

root=$(git rev-parse --show-toplevel 2>/dev/null)

setup_instructions() {
    # $1 = what is missing, $2 = folder
    case "$setup" in
        off)
            echo "Project memory: $1. (Memory setup is off; mention shipshape-adopt once if the user starts real work here.)" ;;
        auto)
            echo "Project memory: $1. **Memory setup is AUTO:** before any code change in this project, set it up yourself"
            echo "with the shipshape-adopt skill (on a branch, docs built from the real code, through a PR), and tell the user in"
            echo "one line that you did. If the user's first message is only a question, answer it first, then set up." ;;
        *)
            if [ -f "$declined" ] && grep -qxF "$2" "$declined" 2>/dev/null; then
                echo "Project memory: $1 (the user declined setup for this folder earlier; don't offer again)."
            else
                echo "Project memory: $1. **Offer once**, in one line at the start of your first reply: \"This project has no"
                echo "memory docs yet - shall I set them up (shipshape-adopt)?\" If they say yes, run the shipshape-adopt skill."
                echo "If they say no, record it so it is never offered again: mkdir -p \"$data\" && echo \"$2\" >> \"$declined\""
            fi ;;
    esac
}

# Never act on a home folder or a drive root.
case "$dir" in
    "$HOME"|"$HOME/"|/|[A-Za-z]:/|[A-Za-z]:\\) echo "(Not a project folder; shipshape stays quiet here.)"; exit 0 ;;
esac

if [ -z "$root" ]; then
    entries=$(ls -A 2>/dev/null | grep -vE '^(\.git|\.claude|\.DS_Store|Thumbs\.db|desktop\.ini)$' | head -n 1)
    if [ -z "$entries" ]; then
        echo "Empty folder: this is a NEW project. When the user asks to build anything here, start with the"
        echo "shipshape-adopt new-project flow (git, memory docs, hooks, CI) before writing the first feature."
        [ "$setup" = "off" ] && echo "(Memory setup is off: ask the user before setting anything up.)"
    else
        setup_instructions "this folder has files but no git repository and no memory docs" "$dir"
    fi
    exit 0
fi

cd "$root" 2>/dev/null || exit 0

if [ ! -f docs/STATUS.md ]; then
    setup_instructions "not set up (no docs/STATUS.md)" "$root"
    echo ""
fi

# Live state: the repo's own report if it has one, else the bundled copy.
if [ -f .shipshape/context.sh ]; then
    sh .shipshape/context.sh 2>/dev/null
else
    sh "$here/skills/shipshape-adopt/assets/shipshape/context.sh" 2>/dev/null
fi
echo ""

if [ "$guard" = "block" ]; then
    branch=$(git branch --show-current 2>/dev/null)
    case "$branch" in
        main|master) echo "Git guard is BLOCK: do not edit files on '$branch'. Create a branch first (ask the user for the name if unsure)." ;;
    esac
fi

# The memory itself. If CLAUDE.md already imports the docs, Claude has them; otherwise put them in context here.
if [ -f docs/STATUS.md ]; then
    if [ -f CLAUDE.md ] && grep -q '@docs/STATUS.md' CLAUDE.md 2>/dev/null; then
        echo "Project memory: CLAUDE.md imports docs/STATUS.md, DECISIONS.md and ARCHITECTURE.md. If their content is not in your context, read them now, before anything else."
    else
        echo "## Project memory: docs/STATUS.md"
        echo ""
        head -n 150 docs/STATUS.md
        echo ""
        if [ -f docs/DECISIONS.md ]; then
            echo "## Project memory: decisions (titles only; read docs/DECISIONS.md in full before changing related code)"
            grep -E '^(\*\*|## |### )D-[0-9]+' docs/DECISIONS.md | cut -c1-200 | head -n 80
            echo ""
        fi
        echo "Read docs/ARCHITECTURE.md before changing code (it maps how the code connects)."
    fi
fi
exit 0
