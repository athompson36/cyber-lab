# Agent Docker Context — Images, Containers, Status & Actions

**Purpose:** Guidance for Docker in the lab: status, container list, start/stop/restart, which images matter, and what is acceptable when advising or implementing.

**Primary production:** The Cyber-Lab stack runs on **fs-dev (192.168.4.100)**. Deploy with `./scripts/deploy-cyber-lab-to-fs-dev.sh`; then open **http://192.168.4.100:5050** in a browser. All hardware (USB for flash, 4K webcam for Workspace) is attached to fs-dev. Running the app locally on a Mac is a **development** option (no USB/camera unless passed through).

---

## 1. Status & availability

- **Endpoint:** GET `/api/docker/status`. Returns: `docker_available` (bool), `docker_message` (string), `images` (list of `repo:tag` for lab images).
- **Check:** Backend runs `docker version --format '{{.Server.Version}}'`. If the app runs **inside** a container, the host Docker daemon is not visible unless the socket is mounted (e.g. `-v /var/run/docker.sock:/var/run/docker.sock`). When unavailable, the UI shows a message like "Unavailable (app in container; mount host Docker socket to see status)".

---

## 2. Lab images (recognized)

| Image name       | Purpose |
|------------------|---------|
| cyber-lab-mcp    | MCP server for Cursor (project context, tools). |
| cyber-lab-web    | Web app (Flask): inventory, flash, Workspace, projects. Preferred name. |
| inventory-app / app-inventory | Legacy names for the same web app (backward compatible). |
| platformio-lab   | PlatformIO build image for firmware. |

Backend filters `docker images` to these prefixes: `cyber-lab-mcp`, `cyber-lab-web`, `inventory-app`, `app-inventory`, `platformio-lab`. Containers are filtered by image name or container name containing "inventory", "cyber-lab", "platformio".

---

## 3. Containers list & actions

- **List:** GET `/api/docker/containers`. Returns array of `{ id, name, image, state, status }`. Only lab-related containers (see above). 503 if Docker unavailable.
- **Actions:** POST `/api/docker/containers/<container_id>/<action>` with `action` one of: **start**, **stop**, **restart**. Container ID or name is sanitized (alphanumeric, `-`, `_` only). Returns `{ success, message }` or `{ error }` with 500 on failure.

### Restart policy (auto-start / auto-restart)

Compose files use **`restart: unless-stopped`** so that:

- **Auto-restart:** If a container exits (crash or OOM), Docker restarts it.
- **Auto-start:** After a host reboot, when the Docker daemon starts, containers that were started with `docker compose up -d` will be started again (assuming the daemon is configured to start on boot).

Use `docker compose -f inventory/app/docker-compose.yml up -d` (local) or on fs-dev use `docker compose -f docker/cyber-lab-compose.yml -f docker/cyber-lab-fs-dev.override.yml up -d` (or run `./scripts/deploy-cyber-lab-to-fs-dev.sh`) to run in the background with this behavior.

---

## 4. Rebuild after code changes

- When **inventory app** or **MCP server** code changes, rebuild so running images match:
  ```bash
  ./scripts/rebuild-containers.sh
  ```
  Or manually:
  ```bash
  docker compose -f inventory/app/docker-compose.yml build
  docker compose -f mcp-server/docker-compose.yml build
  ```
- Restart containers (or `docker compose up`) to use new images. Cursor will use a new MCP image on next MCP call after rebuild.

---

## 5. Tools list (GET /api/docker/tools)

Returns `docker_available` and a `tools` array describing:

- **inventory-web** — This UI (run command, type app).
- **mcp-server** — MCP for Cursor; type docker; available if image `cyber-lab-mcp` exists.
- **platformio-lab** — Build image; available if image exists.
- **firmware-updates** — GET /api/updates.
- **build-db** — `python inventory/scripts/build_db.py`.

Use this for "what Docker tools do I have?" guidance.

---

## 6. Acceptable usage

- **Status:** Never throw 500 on Docker failure; return 503 with a clear message for "Docker not available".
- **Actions:** Only allow `start`, `stop`, `restart`. Sanitize container ID to avoid injection.
- **Filtering:** Only show containers that match lab image/name rules; do not expose unrelated containers.

---

## 7. Ensure services (rebuild + up)

- **Script:** `./scripts/ensure-lab-services.sh` (from repo root) — Rebuilds images via `rebuild-containers.sh`, then `docker compose -f inventory/app/docker-compose.yml up -d`.
- **MCP tool:** `ensure_lab_services` — Same as above; call from Cursor to keep Docker current and inventory app running. Optional arg `rebuild: false` to only bring up containers without rebuilding.
- **Auto-start at login (macOS):** Copy `scripts/com.fstech.ensure-lab-services.plist` to `~/Library/LaunchAgents/`, fix paths in the plist, then `launchctl load ~/Library/LaunchAgents/com.fstech.ensure-lab-services.plist`. See [scripts/README-ensure-lab-services.md](../scripts/README-ensure-lab-services.md).

## 8. When to use this context

- User asks how to **see Docker status**, **start/stop a container**, or **why status is unavailable** (e.g. app in container, socket not mounted).
- User asks **which images to build** or **how to rebuild** after code changes.
- User wants **all containers running and Docker current with code** — use `ensure_lab_services` or run `ensure-lab-services.sh`.
- Implementing or advising **Docker-related API or UI** (Docker & tools tab).
