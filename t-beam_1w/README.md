# T-Beam 1W firmware (lab layout)

Firmware for the LilyGO T-Beam 1W lives here. **These directories are gitignored**; clone upstream into them per [CONTEXT.md](../CONTEXT.md):

```bash
# MeshCore (T-Beam 1W variant)
git clone https://github.com/meshcore-dev/MeshCore.git "t-beam 1w meshcore"

# Meshtastic (port/variant for tbeam-1w)
git clone https://github.com/meshtastic/firmware.git meshtastic-tbeam-1w-firmware/firmware
```

Device context, pinmaps, and tooling: [../devices/t_beam_1w/](../devices/t_beam_1w/).
