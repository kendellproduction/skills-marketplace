#!/usr/bin/env bash
# Install skills from this marketplace into the local Claude skills directory.
#
#   ./install.sh            # install everything
#   ./install.sh council    # install one skill
#
# Safe to re-run — it replaces the installed copy with the current repo version.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

mkdir -p "$DEST"

install_one() {
  local name="$1"
  local src="$SKILLS_SRC/$name"
  if [[ ! -d "$src" ]]; then
    echo "!! no such skill: $name" >&2
    return 1
  fi
  rm -rf "${DEST:?}/$name"
  cp -R "$src" "$DEST/$name"
  echo "   installed $name -> $DEST/$name"
}

if [[ $# -gt 0 ]]; then
  for s in "$@"; do install_one "$s"; done
else
  echo "installing all skills:"
  for d in "$SKILLS_SRC"/*/; do
    install_one "$(basename "$d")"
  done
fi

# Council needs a data directory outside the repo for private context.
if [[ -d "$DEST/council" ]]; then
  DATA="$HOME/.claude/council-data"
  mkdir -p "$DATA/context" "$DATA/notes" "$DATA/sessions"
  if [[ ! -f "$DATA/context/profile.md" ]]; then
    cp "$DEST/council/context-profile.template.md" "$DATA/context/profile.md"
    echo ""
    echo "   Council data dir created at $DATA"
    echo "   -> Fill in $DATA/context/profile.md before your first session."
    echo "      It is private to this machine and is never committed."
  fi
fi

echo ""
echo "done. Restart Claude to pick up new skills."
