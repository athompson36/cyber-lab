# Device Context — Raspberry Pi 4 Model B

**Device ID:** `raspberry_pi_v4`  
**Board:** Raspberry Pi 4 Model B (BCM2711, 40-pin GPIO)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Raspberry Pi 4 uses BCM2711 (quad-core Cortex-A72, 64-bit, 1.5–1.8 GHz), 1–8 GB LPDDR4. Same 40-pin HAT-compatible GPIO header. Runs Linux; build with ARM64 cross-compiler in container.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | BCM2711 (Cortex-A72, 64-bit, 1.5–1.8 GHz, 1–8 GB LPDDR4) |
| **GPIO** | 40-pin header, 3.3 V logic; same pinout as Pi Zero 2 W / Pi 5 |
| **Storage** | microSD; USB boot supported |
| **Connectivity** | Gigabit Ethernet, WiFi, Bluetooth 5.0, USB 2.0/3.0, dual micro HDMI |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | 40-pin header, power |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI, PWM |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | Free pins, 3.3 V |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |

---

## Build in Lab

Use **platformio-lab** with `gcc-aarch64-linux-gnu` for 64-bit builds.
