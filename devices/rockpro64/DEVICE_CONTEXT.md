# Device Context — RockPro64

**Device ID:** `rockpro64`  
**Board:** PINE64 RockPro64 (Rockchip RK3399, 64-bit ARM)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

RockPro64 uses RK3399 (hexa-core Cortex-A72 + Cortex-A53, 64-bit), 2–4 GB DDR4. 40-pin GPIO (RPi-compatible) plus PCIe. Runs Linux (Armbian, Ayufan, mainline). Build with aarch64 cross-compiler.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | RK3399 (A72×2 + A53×4), 2–4 GB DDR4 |
| **GPIO** | 40-pin RPi-compatible; 3.3 V |
| **Storage** | microSD, eMMC; NVMe via PCIe |
| **Connectivity** | Gigabit Ethernet, HDMI, USB 3.0, PCIe |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | 40-pin header |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | 3.3 V |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |
