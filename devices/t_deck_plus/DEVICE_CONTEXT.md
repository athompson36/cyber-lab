# Device Context — T-Deck Plus

**Device ID:** `t_deck_plus`  
**Board:** LilyGO T-Deck Plus (ESP32-S3, keyboard, display, LoRa, etc.)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

T-Deck Plus is a first-class platform in this lab (see [CONTEXT.md](../../CONTEXT.md)). It has a dedicated **launcher** firmware project and **maps** dataset (e.g. OSM tiles). Meshtastic and community firmware support it; map tile generation and launcher are separate repos.

---

## Layout (per CONTEXT.md)

```
t_deck_plus/
├── firmware/
├── launcher/        # Launcher firmware project
├── maps/
│   └── osm_tiles/   # Map datasets (immutable; do not delete/compress/reorganize)
├── configs/
├── pinmaps/
└── notes/
```

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | Pinout / hardware (placeholder; fill from schematic). |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | Peripherals (placeholder). |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | Prototyping notes. |
| [notes/SDK_AND_TOOLS.md](notes/SDK_AND_TOOLS.md) | SDKs, tools, Docker dependencies. |
| [firmware/README.md](firmware/README.md) | **Launcher, map tile generator, Meshtastic, docs.** |

---

## Maps policy

Maps are immutable datasets. Do **not** delete, compress, reorganize, deduplicate, or convert formats without explicit approval. Datasets may exceed 100 GB.

---

## Repos quick reference

- **Launcher:** [bmorcelli/Launcher](https://github.com/bmorcelli/Launcher)
- **Map tiles:** [JustDr00py/tdeck-maps](https://github.com/JustDr00py/tdeck-maps)
- **Launcher docs:** [bmorcelli.github.io/Launcher](https://bmorcelli.github.io/Launcher/)
- **Meshtastic:** [github.com/meshtastic](https://github.com/meshtastic)
