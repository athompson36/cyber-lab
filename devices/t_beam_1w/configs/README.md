# T-Beam 1W — Configs

This folder holds **configuration examples** for the T-Beam 1W:

- **Build/config presets** — e.g. region (868/915 MHz), default passwords, advert names.
- **Channel or mesh configs** — export/import for MeshCore or Meshtastic.
- **Device-specific defaults** — battery limits, display, GPS baud, etc.

## Structure (suggested)

```
configs/
├── meshcore/
│   ├── repeater_example.env    # Build-flags style defaults for repeater
│   ├── room_server_example.env
│   └── companion_example.env
├── meshtastic/
│   └── (future: protobuf or config exports)
└── README.md                  # This file
```

## Current firmware locations

- **MeshCore:** `t-beam_1w/t-beam 1w meshcore` — env defaults are in `platformio.ini` per env (e.g. `ADMIN_PASSWORD`, `ROOM_PASSWORD`, `ADVERT_NAME`).
- **Meshtastic:** `t-beam_1w/meshtastic-tbeam-1w-firmware` — config applied at runtime via app or serial.

Copy or adapt values from those locations into files here for versioned, shareable presets.
