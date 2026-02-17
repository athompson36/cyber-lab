#!/usr/bin/env bash
# Rebuild all lab containers after code changes. Run from repo root.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Rebuilding inventory app..."
docker compose -f inventory/app/docker-compose.yml build

echo "Rebuilding MCP server..."
docker compose -f mcp-server/docker-compose.yml build

echo "Done. Start with: docker compose -f inventory/app/docker-compose.yml up"
