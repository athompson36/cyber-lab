# Embedded Firmware Lab

Unified development environment for **ESP32**, **Arduino**, **Teensy**, **Raspberry Pi**, **Pine64**, and related hardware. Local-first, containerized builds; flash and serial from host (macOS).

---

## What this repo is

- **Lab layout and contract** — devices, firmware overlays, pinmaps, configs, notes.
- **Device context** — per-board hardware layout, peripherals, prototyping, SDKs/tools, firmware repos.
- **Docker** — single `platformio-lab` image for building all supported targets.
- **Docs** — CONTEXT (philosophy and rules), FEATURE_ROADMAP, FIRMWARE_INDEX, REPOS, current projects.

Not a single firmware: it’s the **lab** that holds (or points to) firmware, configs, and tooling.

---

## Quick start

### 1. Build in container

```bash
docker build -t platformio-lab -f docker/Dockerfile .
docker run --rm -v "$(pwd):/workspace" -w /workspace platformio-lab pio run -e T_Beam_1W_SX1262_repeater
```

(Replace env with your target; see [docker/README.md](docker/README.md).)

### 2. Flash from host

Prefer flashing on the host (USB is more reliable than Docker passthrough):

```bash
esptool --chip esp32s3 --port /dev/cu.usbmodem* write_flash 0x0 path/to/firmware.bin
```

### 3. Device and firmware docs

- **Devices:** [devices/README.md](devices/README.md) — list and contract.
- **Firmware index:** [FIRMWARE_INDEX.md](FIRMWARE_INDEX.md) — all firmwares and repos per device.
- **SDKs & tools:** [docker/TOOLS_AND_SDK.md](docker/TOOLS_AND_SDK.md).
- **Current projects:** [current_project.md](current_project.md).

---

## Key docs

| Doc | Purpose |
|-----|--------|
| [CONTEXT.md](CONTEXT.md) | Philosophy, layout, device contract, containers, rules. |
| [FEATURE_ROADMAP.md](FEATURE_ROADMAP.md) | Lab and device roadmap, priorities. |
| [REPOS.md](REPOS.md) | Repo index (Meshtastic, MeshCore, Launcher, etc.). |
| [current_project.md](current_project.md) | ESP32 & SBC project list and lab context. |
| [inventory/README.md](inventory/README.md) | Hardware catalog: SBCs, controllers, sensors, accessories, components (specs + datasheets). |

### Rebuild containers after code changes

When you change the **inventory app** or **MCP server** code, rebuild the images so containers use the latest code:

```bash
./scripts/rebuild-containers.sh
```

Then start the inventory app with `docker compose -f inventory/app/docker-compose.yml up` (or `up --build` to build and start in one step).

---

## Devices

Supported boards live under [devices/](devices/). Each has `DEVICE_CONTEXT.md`, pinmaps, peripherals, prototyping notes, SDK/tools, and firmware links. Examples:

- **t_beam_1w** — LilyGO T-Beam 1W (MeshCore, Meshtastic).
- **t_deck_plus** — T-Deck Plus (Launcher, maps, Meshtastic).
- **raspberry_pi_***, **pine64**, **arduino_uno**, **teensy_v3/v4** — see [devices/README.md](devices/README.md).

---

## License

See [LICENSE](LICENSE). Lab docs and structure are MIT; embedded firmware repos (MeshCore, Meshtastic, etc.) keep their own licenses.
