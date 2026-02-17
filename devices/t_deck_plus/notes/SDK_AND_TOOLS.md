# T-Deck Plus — SDKs & Tools

**Device:** LilyGO T-Deck Plus  
**Container:** platformio-lab (Launcher/Meshtastic) or future esp-idf-lab (LVGL/ESP-IDF)  
**Current projects:** LoRa mesh (2), maps/Launcher.

---

## Build (in container)

| Tool / SDK | Purpose |
|------------|--------|
| **Launcher** | LVGL, ESP-IDF, Rust, or MicroPython — see [bmorcelli/Launcher](https://github.com/bmorcelli/Launcher). |
| **Meshtastic** | PlatformIO, env e.g. `t-deck-tft`. |
| **Map tiles** | [JustDr00py/tdeck-maps](https://github.com/JustDr00py/tdeck-maps) — generator; run where Python/pip available. |

---

## Flash & serial (host)

| Tool | Purpose |
|------|---------|
| **esptool** | Flash Launcher or Meshtastic (T-Deck Plus). Download mode: hold trackball, power on. |
| **Serial** | Config, Meshtastic/Launcher CLI. |

---

## Docker dependencies (platformio-lab)

- PlatformIO, esptool, pyserial, picocom/screen.  
- For Launcher ESP-IDF native: consider esp-idf-lab with ESP-IDF + LVGL.

See [docker/TOOLS_AND_SDK.md](../../../docker/TOOLS_AND_SDK.md).
