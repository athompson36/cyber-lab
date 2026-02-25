# Cyber-Lab: Migration to fs-dev + Full Repo Rename (esp32 → cyber-lab)

This document provides a **systematic plan** to:

1. **Migrate** the full system to a single cyber-lab Docker stack on **fs-dev (192.168.4.100)**, with all hardware attached to fs-dev’s USB ports and the frontend served from the container and accessed by browser.
2. **Rename** the project and repository from **esp32** to **cyber-lab** everywhere (code, docs, images, repo, paths).

It is based on [FS-Tech_Cyber-Lab_Master_Plan.md](FS-Tech_Cyber-Lab_Master_Plan.md) and the current codebase layout.

---

# Part A: Migration to fs-dev (Cyber-Lab Container)

## A.1 Target Architecture (from Master Plan)

- **Host:** fs-dev (192.168.4.100) only. No “run on Mac, flash from Mac” as primary flow; all USB devices and the 4K webcam are on fs-dev.
- **Stack:** One coherent Docker Compose stack (or a small set of compose files) that includes:
  - **cyberlab-ui** — Web frontend (current Flask app UI, later possibly split to static + API).
  - **cyberlab-api** — Backend (current Flask app; Master Plan mentions FastAPI later — can stay Flask until a deliberate migration).
  - **postgres** — Primary data store (replacing or supplementing SQLite for scale and EDU/reporting).
  - **redis** — Event/messaging (for voice, vision, future EDU pipeline).
  - **vision-service** — 4K camera, object detection (YOLOv8), inventory-aware (current Workspace tab + future overlay).
  - **voice-service** — Wake word, STT (Whisper), intent, TTS (future).
  - **flash-service** — esptool, platformio, dfu-util, openocd, pyserial; USB passthrough for devices plugged into fs-dev.
  - **edu-module** — Capture, grading, review (future).
- **Access:** Users open `http://192.168.4.100:<port>` (or a single ingress port) in a browser. No expectation that the app runs on a laptop with its own USB/camera.

## A.2 Current State vs Target

| Area | Current | Target (fs-dev) |
|------|--------|------------------|
| App host | Mac or fs-dev; path_settings can point to Mac paths | fs-dev only; paths always under `/workspace` (mounted repo) or container volumes |
| Database | SQLite `inventory/inventory.db` | Keep SQLite for inventory initially; add Postgres when EDU/reporting is introduced |
| Frontend | Flask-served templates + static (inventory/app) | Same, hosted inside container on fs-dev; browser → fs-dev:5050 |
| USB / flash | Flash from host (Mac); optional Docker USB passthrough | All flashing from fs-dev container via USB passthrough to host devices |
| Webcam | Optional; Workspace tab when app runs on machine with camera | 4K webcam on fs-dev; always available in container via device passthrough |
| MCP server | Runs via Cursor (local or Docker); reads repo | Can run in Docker on fs-dev or remain local; repo cloned/synced to fs-dev |
| Build (firmware) | platformio-lab / esp-idf-lab; build in container, flash from host | Build and flash both on fs-dev (container with USB + repo mount) |

## A.3 Phased Migration Plan

### Phase A.3.1 — Single compose stack on fs-dev (current app + camera + USB)

**Goal:** One `docker compose up` on fs-dev runs the full “lab” experience: UI, API, DB, Workspace camera, and flash capability.

1. **Define canonical compose stack**
   - Create `docker/cyber-lab-compose.yml` (or `docker-compose.cyber-lab.yml` at repo root) that:
     - Uses a single `workspace` mount: repo (or a copy) at `/workspace` on fs-dev.
     - Sets `REPO_ROOT=/workspace` (and `CYBER_LAB_REPO_ROOT=/workspace` for MCP if run in same stack).
   - Services:
     - **web** (current inventory app): Flask app, port 5050; mount repo; **devices: /dev/video0, /dev/ttyUSB*, /dev/ttyACM*** (or dynamic USB); Docker socket only if needed for “list other containers.”
     - Optionally: **mcp** (MCP server image) if you want it to run on fs-dev; else keep MCP for Cursor on dev machine only.
   - Ensure `path_settings.json` is not required for normal operation: default all paths to `REPO_ROOT`-relative paths so that on fs-dev no Mac paths are ever used.

2. **Code and config changes for “fs-dev primary”**
   - **config.py / path_settings:**
     - When `REPO_ROOT == "/workspace"` (or env `CYBER_LAB_HOST=fs-dev`), ignore or override `path_settings.json` for backend/database/frontend paths so they always use `/workspace/...`.
     - Option: on first run in container, write a minimal `path_settings.json` with `/workspace` paths so UI shows correct values.
   - **Flash / serial:**
     - `flash_ops.py` (or equivalent) must use serial ports visible inside the container (e.g. `/dev/ttyUSB0`, `/dev/ttyACM0`). List ports from inside the container; remove any assumption that “host” is a Mac with `/dev/cu.*`.
     - Ensure esptool, pyserial, and (if used) platformio/dfu-util/openocd are available in the image that runs flash.
   - **Workspace (camera):**
     - Already using OpenCV and device passthrough; ensure compose always passes `/dev/video0` (and optionally more video devices) in the fs-dev stack.
   - **Deploy script:**
     - `scripts/deploy-inventory-to-server.sh` becomes the “deploy cyber-lab to fs-dev” script: sync repo to fs-dev, run the new canonical compose (with both compose + override or a single compose that includes devices). Optionally remove `path_settings.json` on server so only `/workspace` paths are used.

3. **Documentation**
   - Update PROJECT_STRUCTURE.md, AGENT_DOCKER_CONTEXT.md, and README to state that the **primary production setup** is: run the cyber-lab stack on fs-dev; open `http://192.168.4.100:5050` in a browser; all hardware is attached to fs-dev.
   - Keep “run locally on Mac” as a **development** option (without USB/camera unless you pass them through).

**Exit criteria:** From a clean clone/sync on fs-dev, `docker compose -f ... up -d` brings up the app; browser to fs-dev:5050 shows UI, inventory, Workspace (camera), and flash targets; flashing a device connected to fs-dev works from the UI.

---

### Phase A.3.2 — Postgres + Redis (optional, for EDU and scale)

**Goal:** Introduce Postgres and Redis without breaking existing inventory (SQLite can remain for inventory initially).

1. Add **postgres** and **redis** services to the same compose file; expose only to internal network (no host ports unless needed for debugging).
2. Add env vars for connection strings (e.g. `DATABASE_URL` for Postgres, `REDIS_URL` for Redis); keep Flask app working with SQLite for inventory until EDU/reporting is implemented.
3. When building EDU module or reporting, add models and migrations for Postgres; optionally migrate inventory to Postgres later or keep SQLite for inventory and use Postgres only for EDU/review/analytics.

**Exit criteria:** Stack starts with Postgres and Redis; app still works with SQLite; EDU/reporting can use Postgres when built.

---

### Phase A.3.3 — Vision, voice, flash as separate services (Master Plan alignment)

**Goal:** Align with Master Plan services: vision-service, voice-service, flash-service.

1. **flash-service**
   - Extract flash/orchestration into a small service (or keep inside the main app but with a clear API). Ensure it runs in a container that has USB passthrough (same as “web” or a dedicated service with device access). API: “flash device X with firmware Y” (and list serial ports).
2. **vision-service**
   - Current Workspace MJPEG + camera list can stay in the main app initially. When adding YOLOv8 or overlay, either:
     - Integrate into the same Flask app (vision routes + OpenCV/YOLO), or
     - Add a separate vision-service container (Python/Node) that reads camera, runs detection, and exposes an API; UI calls it for overlay/annotations.
3. **voice-service**
   - New service: wake word → STT → intent → TTS. Compose adds the service; UI gets a “voice” tab or integration that talks to it. Redis can be used for event/message passing if needed.

**Exit criteria:** Compose defines vision, voice, flash as in the Master Plan; at least flash (and current camera) working end-to-end on fs-dev.

---

### Phase A.3.4 — EDU module (capture, grading, review)

**Goal:** Teacher document capture, grading, review workflow as in Master Plan.

- Implement EDU module (capture, grading, review, reporting) per Master Plan; store data in Postgres; use Redis if needed for async jobs.
- This is a product/feature phase; technical dependency is A.3.2 (Postgres/Redis) and A.3.3 (optional vision for document capture).

---

## A.4 Code and Config Checklist (fs-dev as primary)

- [x] **Compose:** Single canonical compose file (or base + override) for fs-dev that includes: web (Flask), optional MCP, USB devices (`/dev/ttyUSB*`, `/dev/ttyACM*`), `/dev/video0`, mount repo at `/workspace`. Implemented: `docker/cyber-lab-compose.yml` + `docker/cyber-lab-fs-dev.override.yml` (video0; add ttyUSB/ttyACM in override as needed).
- [x] **REPO_ROOT:** All code assumes `REPO_ROOT` is set (e.g. `/workspace`) in container; no reliance on Mac paths in production.
- [x] **path_settings.json:** Defaults or overrides when running in container so database_path, backend_path, frontend_path are under `REPO_ROOT`; avoid syncing Mac path_settings to fs-dev (or clear them in deploy script). Implemented: when `REPO_ROOT=/workspace` or `CYBER_LAB_HOST=fs-dev`, config uses defaults only; deploy script clears path_settings on server.
- [x] **Serial port listing:** Use `/dev/ttyUSB*`, `/dev/ttyACM*` (and any platform-specific names on Linux) in flash_ops / serial listing; do not assume `/dev/cu.*`. Already supported in `flash_ops._list_serial_ports_fallback()`.
- [x] **Flash:** Build and flash both runnable from container; USB passthrough for the container that runs esptool/platformio. Override can add device lines for ttyUSB0/ttyACM0; esptool/pyserial in web image.
- [x] **Camera:** Device passthrough for `/dev/video0` (and optionally more) in the service that serves the Workspace stream. In `docker/cyber-lab-fs-dev.override.yml`.
- [x] **Deploy script:** Single script (e.g. `scripts/deploy-cyber-lab-to-fs-dev.sh`) that: syncs repo to fs-dev, optionally clears path_settings, runs `docker compose -f ... up -d` with the canonical stack.
- [x] **Docs:** README, PROJECT_STRUCTURE, AGENT_DOCKER_CONTEXT updated to describe fs-dev as the primary deployment target and browser access.

---

# Part B: Rename Project and Repo (esp32 → cyber-lab)

## B.1 Scope of Rename

Rename the project and repository from **esp32** to **cyber-lab** everywhere that is user- or tooling-facing, and where it affects paths or image names. Do **not** rename third-party or device-specific references (e.g. “ESP32” chip name, “esp-idf”, “platformio.ini” env names like `t-beam-1w`).

**In scope:**

- Repository name: `esp32` → `cyber-lab` (GitHub/Git: rename repo and default branch clone path).
- Directory name: local clone `esp32/` → `cyber-lab/` (or keep as-is and only change repo name; see below).
- Documentation: all references to “esp32” as the **project/repo name** (e.g. “repo: athompson36/esp32”) → “cyber-lab” and new repo URL.
- Scripts and configs: paths like `~/esp32` → `~/cyber-lab` where they denote the project root.
- Docker: image and container names that today are “inventory-app”, “app-inventory”, “cyber-lab-mcp” can be standardized to a `cyber-lab/*` or `cyberlab/*` prefix (e.g. `cyber-lab-web`, `cyber-lab-mcp`, `cyber-lab-platformio`).
- Python/Node: package or app names (e.g. `inventory_app` in pyproject.toml) can become `cyberlab_web` or stay as-is; MCP is already “cyber-lab-mcp-server”.
- Cursor/IDE: MCP config, rules, and any paths that point at the repo (e.g. `fs-tech/esp32`) → `fs-tech/cyber-lab`.

**Out of scope (do not rename):**

- “ESP32” as chip or board name (e.g. “ESP32-S3”, “esp32s3” in flash_ops, platformio envs).
- Submodule or external repo names (e.g. Meshtastic, MeshCore) unless they are part of this repo.
- File names that are generic (e.g. `config.py`) unless they are tied to the product name.

## B.2 Phased Rename Plan

### Phase B.2.1 — Repo and directory (GitHub + local)

1. **GitHub**
   - Rename repository from `esp32` to `cyber-lab` (Settings → Repository name). Update default branch if needed. Note: clone URL becomes `.../cyber-lab.git`; old `.../esp32.git` may redirect.
2. **Local clone**
   - Either:
     - Rename local directory: `mv esp32 cyber-lab` and update any scripts/IDE that hardcode `esp32`; or
     - Re-clone as `cyber-lab` and re-attach remotes.
   - Update `.cursor/rules`, MCP config, and any absolute paths in docs/scripts that assume `esp32` in the path (e.g. `Documents/fs-tech/esp32` → `Documents/fs-tech/cyber-lab`).

### Phase B.2.2 — Docs and top-level references

1. **Root and key docs**
   - **README.md:** Title and text: “Cyber-Lab” (already “Cyber-Lab” in first line); replace any “esp32” repo references with “cyber-lab” and new repo URL.
   - **CONTEXT.md, PROJECT_STRUCTURE.md, FEATURE_ROADMAP.md, DEVELOPMENT_PLAN.md, CHANGELOG.md, PROJECT_CONTEXT.md:** Replace “esp32” as project/repo name and “athompson36/esp32” with “cyber-lab” and new repo path (e.g. `athompson36/cyber-lab` or org/cyber-lab).
   - **PROJECT_STRUCTURE.md:** Directory tree: change root folder label from `esp32/` to `cyber-lab/`.
   - **docs/AGENT_*.md, docs/INSTALL.md:** Replace repo name and paths (esp32 → cyber-lab).
   - **docs/FS-Tech_Cyber-Lab_Master_Plan.md:** Already “Cyber-Lab”; ensure consistency.

2. **Scripts**
   - **scripts/deploy-inventory-to-server.sh:** `~/esp32` → `~/cyber-lab` (or parameterize REPO_DIR).
   - **scripts/run-inventory-app-on-server.sh:** `REPO_ROOT="${REPO_ROOT:-$HOME/esp32}"` → `$HOME/cyber-lab`.
   - **scripts/README-ensure-lab-services.md, com.fstech.ensure-lab-services.plist:** Replace example path `.../esp32` with `.../cyber-lab`.
   - Any other script that assumes project directory name `esp32`.

### Phase B.2.3 — Docker image and service names

1. **Compose and Dockerfiles**
   - **inventory/app/docker-compose.yml:** Service name `inventory` → e.g. `web` or `cyberlab-web`; image name `app-inventory` → e.g. `cyber-lab-web` (align with Master Plan “cyberlab-ui” / “cyberlab-api” if you split later).
   - **mcp-server/docker-compose.yml:** Image already `cyber-lab-mcp`; service name can stay `mcp` or become `cyber-lab-mcp`.
   - **docker/** (platformio-lab, esp-idf-lab): Image names can stay as-is or become `cyber-lab-platformio`, `cyber-lab-esp-idf` for consistency.
   - Update **app.py** (and any code) that filters Docker images/containers by name: include new names (e.g. `cyber-lab-web`, `cyber-lab-mcp`) and keep backward compatibility with `app-inventory`, `inventory-app` during transition.

2. **Rebuild and deploy**
   - **scripts/rebuild-containers.sh:** Build the images with new names (e.g. `cyber-lab-web`, `cyber-lab-mcp`).
   - **scripts/deploy-inventory-to-server.sh** (or new `deploy-cyber-lab-to-fs-dev.sh`): Sync to `~/cyber-lab`, run compose with new service/image names.

### Phase B.2.4 — Python/Node package and internal names

1. **Python**
   - **inventory/app/pyproject.toml:** If the package/project is named `inventory_app` or `esp32`-related, rename to e.g. `cyberlab-web` or `cyberlab_api` (optional; can stay `inventory_app` and only change Docker/service names).
   - **inventory/scripts/build_db.py:** No “esp32” in product name; leave as-is unless you rename the inventory app package.

2. **Node (MCP)**
   - **mcp-server/package.json:** `name` already “cyber-lab-mcp-server”; ensure no “esp32” in name or description.
   - **cursor-mcp-example*.json:** Paths and descriptions: “cyber-lab” instead of “esp32” or “cyber-lab” repo path.

### Phase B.2.5 — CI and external references

1. **GitHub Actions**
   - Workflow files under `.github/workflows/`: Replace `esp32` repo name in checkout paths or comments with `cyber-lab`; ensure checkout uses correct repo and ref.
   - Any artifact or job names that say “esp32” → “cyber-lab”.

2. **Misc**
   - **FEATURE_ROADMAP.md, PROJECT_AUDIT.md:** Replace “athompson36/esp32” and “esp32” as repo name.
   - **.cursor/rules:** Paths and repo name in rule text.

## B.3 Rename Checklist

- [ ] **GitHub repo renamed to `cyber-lab`** — Do manually in GitHub Settings → Repository name.
- [x] Local clone directory and all script/IDE paths updated in scripts and plist to use `cyber-lab`.
- [ ] README, CONTEXT, PROJECT_STRUCTURE, FEATURE_ROADMAP, DEVELOPMENT_PLAN, CHANGELOG, PROJECT_CONTEXT, docs/AGENT_*.md, INSTALL.md: “esp32” (as project/repo) → “cyber-lab”; repo URL updated.
- [x] Scripts and plist: path examples and default REPO_ROOT use `cyber-lab`.
- [x] Docker: image `cyber-lab-web` added; app.py and rebuild script updated; backward compatibility kept.
- [x] Python/Node: MCP and cursor examples already cyber-lab; inventory-app pyproject left as-is.
- [x] CI: workflow comment updated.
- [ ] Search codebase for remaining “esp32” as project/repo (not chip/board): `grep -r "esp32" --include="*.md" --include="*.yml" --include="*.json" --include="*.py" --include="*.ts" --include="*.sh" .` and fix.

---

*Part B executed 2026-02-25. GitHub repo rename and local folder rename (e.g. `mv esp32 cyber-lab`) remain manual.*

---

# Part C: Suggested Order of Execution

1. **Rename first (Part B)**  
   Do the repo and project rename (B.2.1–B.2.5) so that all new work and migration refer to “cyber-lab” and the new repo. This avoids double renames and keeps branch/PR naming consistent.

2. **Then migrate to fs-dev (Part A)**  
   Execute A.3.1 (single compose on fs-dev, path and USB/camera assumptions), then A.3.2–A.3.4 as needed. All new compose and scripts use “cyber-lab” naming and `~/cyber-lab` (or equivalent) on fs-dev.

3. **Optional: single “master” compose**  
   After rename and A.3.1, introduce one `docker-compose.yml` (or `docker/cyber-lab-compose.yml`) at repo root that defines the full fs-dev stack (web, mcp if desired, postgres/redis when added, vision/voice/flash services when implemented), so that “run cyber-lab on fs-dev” is one command.

---

# Summary Tables

| Phase | What | Outcome |
|-------|------|--------|
| B.2.1 | Repo + dir rename | GitHub repo `cyber-lab`; local path `.../cyber-lab` |
| B.2.2 | Docs + scripts | All references say “cyber-lab” and new repo URL |
| B.2.3 | Docker names | Images/services: cyber-lab-web, cyber-lab-mcp, etc. |
| B.2.4–B.2.5 | Packages, CI | Consistent naming; CI uses new repo |
| A.3.1 | Single stack on fs-dev | One compose; UI + camera + flash on fs-dev; browser access |
| A.3.2 | Postgres + Redis | Ready for EDU and reporting |
| A.3.3 | Vision/voice/flash services | Aligned with Master Plan services |
| A.3.4 | EDU module | Capture, grading, review, reporting |

---

*Document version: 1.0. Part B (rename) executed 2026-02-25. Part A.3.1 (fs-dev migration) executed 2026-02-25: canonical compose, config overrides, deploy script, docs. Next: A.3.2 (Postgres + Redis) when needed.*
