# Device Context — Pine A64

**Device ID:** `pine64`  
**Board:** Pine A64 / Pine64 (Allwinner A64, 64-bit ARM)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Pine A64 is the original Pine64 SBC: Allwinner A64 (quad-core Cortex-A53, 64-bit), 512 MB–2 GB RAM. Expansion headers for GPIO, I2C, UART, SPI. Runs Linux (Armbian, mainline, Buildroot). Build with aarch64 cross-compiler in container.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | Allwinner A64 (Cortex-A53, 64-bit), 512 MB–2 GB DDR3 |
| **Expansion** | 2× 28-pin headers (Euler bus); GPIO, I2C, UART, SPI |
| **Storage** | microSD, eMMC option |
| **Connectivity** | Ethernet, HDMI, USB |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | Euler connector pinout |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI, GPIO |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | Voltage, expansion |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |
