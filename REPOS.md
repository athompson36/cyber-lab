# Lab Repositories Index

Central index of firmware, tools, and documentation repos used in this lab.

- **Full firmware list (all devices):** [FIRMWARE_INDEX.md](FIRMWARE_INDEX.md)
- **Per-device details:** `devices/<device>/firmware/README.md`

---

## Meshtastic & T-Deck

| Repo | Description |
|------|-------------|
| [meshtastic](https://github.com/meshtastic) | Meshtastic organization — firmware, protos, docs, web, etc. |
| [JustDr00py/tdeck-maps](https://github.com/JustDr00py/tdeck-maps) | Meshtastic map tile generator for the T-Deck. |
| [bmorcelli/Launcher](https://github.com/bmorcelli/Launcher) | Launcher for the T-Deck (first-class firmware project per CONTEXT.md). |
| Launcher docs | [bmorcelli.github.io/Launcher](https://bmorcelli.github.io/Launcher/) — scrape/source for Launcher documentation. |

---

## MeshCore & T-Beam 1W

| Repo | Description |
|------|-------------|
| [meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore) | MeshCore — lightweight multi-hop LoRa library and firmware. |
| [mintylinux/Meshcore-T-beam-1W-Firmware](https://github.com/mintylinux/Meshcore-T-beam-1W-Firmware) | MeshCore T-Beam 1W firmware (community/variant). |

---

## Device mapping

- **T-Deck Plus:** Launcher, tdeck-maps, Meshtastic (device apps/firmware). See [devices/t_deck_plus/firmware/README.md](devices/t_deck_plus/firmware/README.md).
- **T-Beam 1W:** MeshCore (upstream + mintylinux variant), Meshtastic port. See [devices/t_beam_1w/firmware/README.md](devices/t_beam_1w/firmware/README.md).
