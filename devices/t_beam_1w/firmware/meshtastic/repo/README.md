# Meshtastic T‑Beam 1W (ESP32‑S3) — Cursor Starter

This is a **Cursor starter project** to build a custom Meshtastic firmware target for the **LilyGO T‑Beam 1W (ESP32‑S3, USB‑C)**.

The zip does **not** bundle Meshtastic source. Instead, it provides:
- a repeatable clone/build workflow
- templates for a new PlatformIO environment and `variants/tbeam_1w` files
- a place to record the board’s pin mapping

## What you do with this
1. Get firmware: clone the main repo with `git clone --recurse-submodules`, or run `git submodule update --init --recursive`. Meshtastic lives in `./firmware/` as a submodule.
2. (Optional) Apply lab overlays (e.g. T-Deck trackball calibration): `./scripts/apply_lab_patches.sh`
3. Apply the T-Beam 1W templates in `./patches/templates/` (Cursor can do this quickly) and fill in `docs/TBEAM_1W_PINMAP.md`
4. Build with PlatformIO
5. Flash with `esptool` (works reliably on ESP32‑S3)

## Prereqs (macOS)
- Homebrew
- PlatformIO Core: `brew install platformio`
- Python tools for flashing: `pipx install esptool`

## Getting Meshtastic firmware
The main repo tracks Meshtastic as a submodule. From the **main repo root**:

```bash
git submodule update --init --recursive
```

That populates `devices/t_beam_1w/firmware/meshtastic/repo/firmware`. To apply lab patches (T-Deck trackball calibration, etc.) from this directory: `./scripts/apply_lab_patches.sh`.

## Build (after you add the new env)
```bash
cd firmware
pio run -e tbeam-1w
```

## Flash (example)
Put the board in bootloader mode (hold BOOT while plugging in USB; battery disconnected), then:

```bash
esptool --port /dev/cu.usbmodemXXXX erase-flash
esptool --port /dev/cu.usbmodemXXXX write-flash -z 0x0 .pio/build/tbeam-1w/firmware.bin
```

## Notes
- The provided variant/env templates are intentionally conservative. You will likely need to adjust:
  - SX1262 pins (SPI + DIO1/BUSY/RESET)
  - PA/LNA enable pins (1W front end)
  - OLED driver + I2C pins
