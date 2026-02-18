#!/usr/bin/env bash
set -euo pipefail

# Apply lab overlay patches to the Meshtastic firmware submodule.
# Run from repo root after: git submodule update --init --recursive

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIRMWARE="$ROOT/firmware"
PATCHES="$ROOT/patches"

if [[ ! -d "$FIRMWARE/.git" ]]; then
  echo "ERROR: $FIRMWARE is not a git clone. Run: git submodule update --init --recursive" >&2
  exit 1
fi

for p in "$PATCHES"/*.patch; do
  [[ -f "$p" ]] || continue
  echo "Applying $(basename "$p")..."
  ( cd "$FIRMWARE" && git apply -p1 --verbose < "$p" )
done
echo "Lab patches applied."
