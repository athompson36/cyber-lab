# Device Context — Raspberry Pi Zero 2 W

**Device ID:** `raspberry_pi_zero`  
**Board:** Raspberry Pi Zero 2 W (BCM2710A1 SiP, 40-pin GPIO)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Raspberry Pi Zero 2 W uses a BCM2710A1 (quad-core 64-bit ARM Cortex-A53 @ 1 GHz, 512 MB LPDDR2). Same 40-pin HAT-compatible GPIO header as other modern Pi boards. Runs Linux (Raspberry Pi OS, Buildroot, etc.); no bare-metal firmware in the same sense as MCU boards. Build in container with ARM cross-compilers; deploy image to SD or USB.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | BCM2710A1 (Cortex-A53, 64-bit, 1 GHz, 512 MB RAM) |
| **GPIO** | 40-pin header, 3.3 V logic; compatible with Pi 4 pinout |
| **Storage** | microSD |
| **Connectivity** | WiFi, Bluetooth (on-board); Mini HDMI, micro USB (power + data) |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | 40-pin header, power, block diagram |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI, PWM, GPIO usage |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | Free pins, 3.3 V only, HAT compatibility |
| [firmware/README.md](firmware/README.md) | Available OS/firmware repos and build systems |

---

## Build in Lab

Use **platformio-lab** (or dedicated ARM container) with `gcc-aarch64-linux-gnu` for 64-bit builds. Kernel and rootfs are typically built with their own build systems (see firmware/README.md).
