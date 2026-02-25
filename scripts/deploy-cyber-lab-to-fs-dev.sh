#!/usr/bin/env bash
# Deploy Cyber-Lab stack to fs-dev (192.168.4.100). Syncs repo, clears path_settings,
# and starts the canonical compose (web at 5050 with repo at /workspace, webcam, Docker socket).
# For USB serial (flashing), add device lines to docker/cyber-lab-fs-dev.override.yml
# (e.g. - /dev/ttyUSB0:/dev/ttyUSB0) or run scripts/generate-fs-dev-override.sh on the server.
#
# Usage (from repo root):
#   ./scripts/deploy-cyber-lab-to-fs-dev.sh [user@host]
# Example:
#   ./scripts/deploy-cyber-lab-to-fs-dev.sh andrew@192.168.4.100
#
# Then open http://192.168.4.100:5050 — UI, Workspace (camera), and flash (if serial in override) work from the browser.

set -e
SERVER="${1:-andrew@192.168.4.100}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "Syncing repo to $SERVER..."
rsync -az --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  "$REPO_ROOT/" "$SERVER:~/cyber-lab/"

echo "Starting Cyber-Lab stack on server (canonical compose + fs-dev override)..."
ssh "$SERVER" "cd ~/cyber-lab &&
  rm -f artifacts/path_settings.json &&
  docker compose -f inventory/app/docker-compose.yml down 2>/dev/null || true &&
  docker compose -f docker/cyber-lab-compose.yml -f docker/cyber-lab-fs-dev.override.yml down 2>/dev/null || true &&
  docker compose -f docker/cyber-lab-compose.yml -f docker/cyber-lab-fs-dev.override.yml up -d --build"

echo "Done. Open http://$(echo "$SERVER" | cut -d@ -f2):5050"