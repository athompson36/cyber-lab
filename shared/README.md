# Shared — Hardware Intelligence

**Purpose:** Single place for hardware rules, constraints, and notes that apply across firmware (MeshCore, Meshtastic, custom) and devices. Device folders under `devices/` reference this for RF/PA, PMU, fan, power, and safety so overlays stay consistent.

## Layout

```
shared/
├── README.md           # This file
└── t_beam_1w/
    ├── README.md       # Index for T-Beam 1W shared notes
    └── RF_PA_FAN_PMU.md  # Radio, PA, fan, PMU rules and specs
```

## Usage

- **Firmware overlays** (e.g. MeshCore variant, Meshtastic board) should follow the constraints in `shared/<device>/`.
- **Device docs** in `devices/<device>/` link to shared for canonical RF/PA/PMU/fan rules; pinmaps and peripherals remain device-local.
- Add a `shared/<device>/` folder when a device has hardware rules that multiple firmwares must respect.
