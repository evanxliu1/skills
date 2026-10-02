#!/bin/sh
# Symlink every skill in ./skills into the personal skill directories of the
# agents installed on this machine. Re-run after adding a skill; existing
# entries that are not symlinks into this repo are left alone.
set -eu
REPO=$(cd "$(dirname "$0")" && pwd)
targets="$HOME/.claude/skills"
[ -d "$HOME/.codex" ] && targets="$targets $HOME/.codex/skills"
for dest in $targets; do
    mkdir -p "$dest"
    for skill in "$REPO"/skills/*/; do
        name=$(basename "$skill")
        link="$dest/$name"
        if [ -L "$link" ]; then
            ln -sfn "${skill%/}" "$link"
        elif [ -e "$link" ]; then
            echo "skip: $link exists and is not a symlink"
            continue
        else
            ln -s "${skill%/}" "$link"
        fi
        echo "linked: $link -> ${skill%/}"
    done
done
