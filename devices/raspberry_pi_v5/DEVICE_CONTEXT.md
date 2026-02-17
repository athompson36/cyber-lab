# Device Context — Raspberry Pi 5

**Device ID:** `raspberry_pi_v5`  
**Board:** Raspberry Pi 5 (BCM2712 + RP1, 40-pin GPIO)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Raspberry Pi 5 uses BCM2712 (quad-core Cortex-A76, 64-bit, 2.4 GHz) and RP1 I/O controller for GPIO and peripherals. Same 40-pin header pinout as Pi 4/Zero 2 W for compatibility. Runs Linux; build with ARM64 cross-compiler.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | BCM2712 (Cortex-A76, 64-bit, 2.4 GHz); RP1 for GPIO/peripherals |
| **GPIO** | 40-pin header, 3.3 V; pinout identical to Pi 4 |
| **Storage** | microSD; USB boot; optional NVMe via PCIe |
| **Connectivity** | Gigabit Ethernet, WiFi, Bluetooth 5.0, USB 3.0, dual HDMI |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | 40-pin header, power |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI, PWM (via RP1) |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | 3.3 V only |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |

---

## Build in Lab

Use **platformio-lab** with `gcc-aarch64-linux-gnu` for 64-bit builds.
