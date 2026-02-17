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

## Device layout: symlink vs copy

**Goal:** Map upstream firmware repos into this device folder so builds and overlays stay under the lab contract.

### Option A — Symlink (current, minimal change)

- Clone repos **outside** this directory (e.g. repo root) so they remain in `.gitignore`.
- **Symlink** from `devices/t_beam_1w/firmware/` into those clones so paths are consistent.

| Firmware   | Clone location (repo root)              | Symlink target |
|------------|------------------------------------------|----------------|
| MeshCore   | `t-beam_1w/t-beam 1w meshcore/`          | `firmware/meshcore/repo` → `../../../t-beam_1w/t-beam 1w meshcore` |
| Meshtastic | `t-beam_1w/meshtastic-tbeam-1w-firmware/`| `firmware/meshtastic/repo` → `../../../t-beam_1w/meshtastic-tbeam-1w-firmware` |

**Pros:** No copy; upstream stays pristine; `.gitignore` already excludes the clone paths.  
**Cons:** You must create the symlinks after cloning (see [t_beam_1w/README.md](../../t_beam_1w/README.md) or repo root README).

### Option B — Copy under firmware/

- Create `firmware/meshcore/repo/` and `firmware/meshtastic/repo/` and **clone or copy** upstream into them.
- Overlays go in `firmware/meshcore/overlays/` and `firmware/meshtastic/overlays/` (patches, platformio env fragments).

**Pros:** Everything for this device lives under `devices/t_beam_1w/firmware/`.  
**Cons:** Duplicates repo; need to pull/merge upstream manually or via script.

### Current state

- **MeshCore (T-Beam 1W variant):** clone at repo root `t-beam_1w/t-beam 1w meshcore/` (gitignored). Build from that path; no symlink under `devices/` yet.
- **Meshtastic (tbeam-1w port):** clone at repo root `t-beam_1w/meshtastic-tbeam-1w-firmware/` (gitignored).

To align with Option A: create `firmware/meshcore/` and `firmware/meshtastic/` here, then add symlinks `meshcore/repo` → `../../../t-beam_1w/t-beam 1w meshcore` and `meshtastic/repo` → `../../../t-beam_1w/meshtastic-tbeam-1w-firmware`. Build from `firmware/<name>/repo` so the orchestrator can use a single pattern per device.

## Build

- **MeshCore:** From the meshcore repo dir, `pio run -e T_Beam_1W_SX1262_repeater` (or `_room_server`, `_companion_radio_ble`).
- **Meshtastic:** From the meshtastic port dir, follow `docs/DEVELOPMENT_PLAN.md` and `pio run -e tbeam-1w` (or the env name used there).

See [FEATURE_ROADMAP.md](../../../FEATURE_ROADMAP.md) for orchestrator and artifact paths. See [REPOS.md](../../../REPOS.md) for the full lab repo index.
