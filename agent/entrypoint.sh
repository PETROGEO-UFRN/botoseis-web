#!/bin/bash
set -e

# ~/.hermes is a volume. The runtime dirs are linked from the image so a rebuild updates
# Hermes; the remaining installer files (.env, SOUL.md, bundled skills, ...) are copied
# only where the volume has no copy yet.
RUNTIME="${HOME}/.hermes-runtime"
for entry in "${RUNTIME}"/* "${RUNTIME}"/.[!.]*; do
    [ -e "${entry}" ] || continue
    name="$(basename "${entry}")"
    case "${name}" in
        hermes-agent|tools|installs) ln -sfn "${entry}" "${HOME}/.hermes/${name}" ;;
        *) cp -an "${entry}" "${HOME}/.hermes/" ;;
    esac
done

# No Claude login stored yet: open a shell to log in manually instead of letting
# Hermes exit (which would stop the container).
if [ ! -s "${CLAUDE_CONFIG_DIR}/.credentials.json" ]; then
    echo "No Claude account login found. Log in, then start Hermes:"
    echo "  claude          -> /login, paste the code, /exit   (persisted)"
    echo "  hermes chat --provider anthropic"
    exec bash
fi

# Resume the most recent session; `-c` exits with an error when there is none.
RESUME=()
if hermes sessions list 2>/dev/null | grep -qE '[0-9]{8}_[0-9]{6}_'; then
    RESUME=(--continue)
fi

# Hermes reuses Claude Code's stored credentials for the Anthropic provider.
exec hermes chat --provider anthropic "${RESUME[@]}"
