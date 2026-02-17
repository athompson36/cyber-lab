# T-Beam 1W — Firmware

Per the lab contract, all firmware for this device lives under this directory, with **overlays** for customisations (no direct edits to upstream repos).

---

## Available firmwares & repos

**Full index:** [FIRMWARE_INDEX.md](../../../FIRMWARE_INDEX.md#t_beam_1w-lilygo-t-beam-1w)

| Firmware / project | Repo | Notes |
|--------------------|------|--------|
| **MeshCore** (upstream) | [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore) | Multi-hop LoRa; Companion, Repeater, Room Server. Also [ripplebiz/MeshCore](https://github.com/ripplebiz/MeshCore). |
| **MeshCore T-Beam 1W** | [mintylinux/Meshcore-T-beam-1W-Firmware](https://github.com/mintylinux/Meshcore-T-beam-1W-Firmware) | Community variant. |
| **Meshtastic** (upstream) | [meshtastic/firmware](https://github.com/meshtastic/firmware) | Official; T-Beam 1W target. |
| **Meshtastic** (LilyGO fork) | [Xinyuan-LilyGO/Meshtastic_firmware](https://github.com/Xinyuan-LilyGO/Meshtastic_firmware) | Device-specific builds. |
| **Prebuilt Meshtastic** | [ksjkl1/LilyGO-TTGO-T-Beam-Meshtastic](https://github.com/ksjkl1/LilyGO-TTGO-T-Beam-Meshtastic) | Binaries + install scripts. |
| **LilyGO examples** | [LilyGO/TTGO-T-Beam](https://github.com/LilyGO/TTGO-T-Beam) | Examples, factory (legacy). |

---

## Target layout (CONTEXT.md)

```
firmware/
├── meshcore/
│   ├── repo/          # Upstream MeshCore clone
│   └── overlays/      # Board variant, PA limits, power profiles
├── meshtastic/
│   ├── repo/          # Upstream Meshtastic firmware clone
│   └── overlays/      # T-Beam 1W variant, platformio env
├── expresslrs/       # (optional)
└── custom/            # Custom firmware
```

## Current locations (before migration)

Until the lab migration is complete, firmware lives at:

- **MeshCore (T-Beam 1W variant):** `../../t-beam_1w/t-beam 1w meshcore`
- **Meshtastic port (tbeam-1w):** `../../t-beam_1w/meshtastic-tbeam-1w-firmware`

After migration, `repo/` will hold the upstream clones and `overlays/` the T-Beam 1W–specific patches and config (variant, platformio env, PA/fan/battery fixes).

## Build

- **MeshCore:** From the meshcore repo dir, `pio run -e T_Beam_1W_SX1262_repeater` (or `_room_server`, `_companion_radio_ble`).
- **Meshtastic:** From the meshtastic port dir, follow `docs/DEVELOPMENT_PLAN.md` and `pio run -e tbeam-1w` (or the env name used there).

See [FEATURE_ROADMAP.md](../../../FEATURE_ROADMAP.md) for orchestrator and artifact paths. See [REPOS.md](../../../REPOS.md) for the full lab repo index.
