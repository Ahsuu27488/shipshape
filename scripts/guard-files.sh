#!/bin/sh
# shipshape PreToolUse guard for Read / Edit / Write (Claude Code).
# Only acts in unattended runs (SHIPSHAPE_UNATTENDED=1): secret files are off limits there.

[ "${SHIPSHAPE_UNATTENDED:-0}" = "1" ] || { cat >/dev/null; exit 0; }
input=$(cat)
path=$(printf '%s' "$input" | tr '\n' ' ' | sed -nE 's/.*"file_path"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/p' | head -n 1)
[ -n "$path" ] || exit 0
name=$(printf '%s' "$path" | sed 's#.*[/\\]##')
case "$name" in
    .env.example|.env.sample|.env.template) exit 0 ;;
    .env|.env.*|id_rsa*|id_ed25519*|*.pem|*.p12|*.pfx|*credentials*|*cookies*.txt|*.keystore)
        printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' \
            "shipshape (unattended): $name looks like a secret. Unattended runs never open secrets; note what you needed in the report."
        ;;
esac
exit 0
