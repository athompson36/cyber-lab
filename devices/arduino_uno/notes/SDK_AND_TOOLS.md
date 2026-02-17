# Arduino Uno — SDKs & Tools

**Device:** Arduino Uno R3 (ATmega328P)  
**Container:** platformio-lab  
**Current projects:** MIDI controller (4), simple control nodes.

---

## Build (in container)

| Tool / SDK | Purpose |
|------------|--------|
| **PlatformIO** | `platform = atmelavr`, `board = uno`. |
| **arduino-cli** | Alternative: `arduino-cli compile --fqbn arduino:avr:uno`. |

---

## Flash (host recommended)

| Tool | Purpose |
|------|---------|
| **avrdude** | Via PlatformIO upload or Arduino CLI; USB serial. |

---

## Docker dependencies (platformio-lab)

- PlatformIO (atmelavr), optional arduino-cli.

See [docker/TOOLS_AND_SDK.md](../../../docker/TOOLS_AND_SDK.md).
