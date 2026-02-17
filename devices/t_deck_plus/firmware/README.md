# T-Deck Plus — Firmware & Repos

Per [CONTEXT.md](../../../CONTEXT.md), the launcher is a first-class firmware project; maps live under `../maps/osm_tiles/` and are immutable.

---

**Full index:** [FIRMWARE_INDEX.md](../../../FIRMWARE_INDEX.md#t_deck_plus-lilygo-t-deck-plus)

## Launcher & maps

| Firmware / project | Repo / URL | Notes |
|--------------------|------------|--------|
| **Launcher** | [bmorcelli/Launcher](https://github.com/bmorcelli/Launcher) | First-class launcher; LVGL/ESP-IDF/Rust/MicroPython. Clone into `launcher/`. |
| **Launcher docs** | [bmorcelli.github.io/Launcher](https://bmorcelli.github.io/Launcher/) | Documentation source. |
| **Map tile generator** | [JustDr00py/tdeck-maps](https://github.com/JustDr00py/tdeck-maps) | Meshtastic map tiles for T-Deck. |

## Meshtastic & hardware

| Firmware / project | Repo | Notes |
|--------------------|------|--------|
| **Meshtastic** (upstream) | [meshtastic/firmware](https://github.com/meshtastic/firmware) | T-Deck / T-Deck Plus (e.g. `t-deck-tft`). |
| **Meshtastic** (LilyGO fork) | [Xinyuan-LilyGO/Meshtastic_firmware](https://github.com/Xinyuan-LilyGO/Meshtastic_firmware) | Device builds. |
| **T-Deck hardware** | [Xinyuan-LilyGO/T-Deck](https://github.com/Xinyuan-LilyGO/T-Deck) | Schematics, board files, examples, TFT_eSPI. |
| **Meshtastic org** | [meshtastic](https://github.com/meshtastic) | Web, Android, Apple, Python, protos, docs. |

---

## Lab layout

- **Launcher:** Prefer cloning [Launcher](https://github.com/bmorcelli/Launcher) into `devices/t_deck_plus/launcher/` (per CONTEXT).
- **Maps:** Store tile datasets in `devices/t_deck_plus/maps/osm_tiles/`. Do not delete, compress, or reorganize without approval.
- **Map tooling:** Use [tdeck-maps](https://github.com/JustDr00py/tdeck-maps) to generate tiles; output can be placed in `maps/osm_tiles/` or documented path.

See also [REPOS.md](../../../REPOS.md) for the full lab repo index.
