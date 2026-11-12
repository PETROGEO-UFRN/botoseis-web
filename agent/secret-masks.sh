#!/bin/sh
# Prints a compose override for boto-dev-agent that hides the repo's secret files
# (.env files, keys) behind /dev/null. Only files that exist get a mount: a bind mount
# whose source is missing would fail, or make the engine create it on the host.
# Run from the repo root; `make agent` writes the output to .secrets/agent-masks.yml.
set -eu

files="$(find . \
    \( -path ./.git -o -path ./.secrets -o -name node_modules \) -prune -o \
    -type f \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' \) \
    ! -name '.env.example' ! -name '.env.sample' ! -name '.env.template' \
    -print | sed 's|^\./||' | sort)"

if [ -z "${files}" ]; then
    echo "services: {}"
    exit 0
fi

echo "services:"
echo "  boto-dev-agent:"
echo "    volumes:"
echo "${files}" | while IFS= read -r file; do
    echo "      - type: bind"
    echo "        source: /dev/null"
    echo "        target: \"/workspace/${file}\""
    echo "        read_only: true"
done
