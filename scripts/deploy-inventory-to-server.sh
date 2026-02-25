#!/usr/bin/env bash
# Deploy and run the inventory app on the server (fs-dev) so the Workspace tab
# can use the server's webcam. Syncs repo, enables camera override, starts containers.
#
# Usage (from repo root):
#   ./scripts/deploy-inventory-to-server.sh [user@host]
# Example:
#   ./scripts/deploy-inventory-to-server.sh andrew@192.168.4.100
#
# Then open http://192.168.4.100:5050 — search, inventory, and Workspace (camera) will work.

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

echo "Enabling webcam override and starting app on server..."
ssh "$SERVER" "cd ~/cyber-lab &&
  cp -n inventory/app/docker-compose.override.server.yml inventory/app/docker-compose.override.yml 2>/dev/null || true &&
  rm -f artifacts/path_settings.json &&
  docker compose -f inventory/app/docker-compose.yml -f inventory/app/docker-compose.override.yml up -d --build"

echo "Done. Open http://$(echo $SERVER | cut -d@ -f2):5050 (Workspace tab = server webcam)."
