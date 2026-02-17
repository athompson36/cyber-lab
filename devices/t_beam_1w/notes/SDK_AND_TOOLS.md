# T-Beam 1W — SDKs & Tools

**Device:** LilyGO T-Beam 1W  
**Container:** platformio-lab  
**Current projects:** LoRa mesh nodes (2), sensor array (5).

---

## Build (in container)

| Tool / SDK | Purpose |
|------------|--------|
| **PlatformIO** | Build MeshCore (Companion, Repeater, Room Server) and Meshtastic. |
| **Platform** | espressif32 (ESP32-S3). |
| **Envs** | `T_Beam_1W_SX1262_repeater`, `_room_server`, `_companion_radio_ble`. |

```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace platformio-lab pio run -e T_Beam_1W_SX1262_repeater
```

---

## Flash & serial (host recommended)

| Tool | Purpose |
|------|---------|
| **esptool** | Flash merged or factory .bin at 0x0 (ESP32-S3). Hold BOOT, connect USB, then flash. |
| **Serial monitor** | screen, picocom, or `pio device monitor` — config/repeater CLI (e.g. `get prv.key`, `set freq`). |

Host install: `pipx install esptool` or `brew install esptool`.

---

## Docker dependencies (platformio-lab)

- **PlatformIO** — build.
- **esptool** — merge_bin, image_info, CI flash.
- **pyserial** — Python serial scripts for config.
- **picocom / screen** — serial console in container if USB passed.

See [docker/TOOLS_AND_SDK.md](../../../docker/TOOLS_AND_SDK.md) and [docker/DEPENDENCIES.md](../../../docker/DEPENDENCIES.md).
