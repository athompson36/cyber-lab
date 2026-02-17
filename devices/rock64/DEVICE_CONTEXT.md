# Device Context — Rock64

**Device ID:** `rock64`  
**Board:** PINE64 Rock64 (Rockchip RK3328, 64-bit ARM)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Rock64 uses Rockchip RK3328 (quad-core Cortex-A53, 64-bit), 1–4 GB DDR3. 40-pin GPIO header (RPi-compatible layout). Runs Linux (Armbian, Ayufan images). Build with aarch64 cross-compiler.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | RK3328 (Cortex-A53, 64-bit), 1–4 GB DDR3 |
| **GPIO** | 40-pin header, RPi-compatible pinout; 3.3 V |
| **Storage** | microSD, eMMC option |
| **Connectivity** | Gigabit Ethernet, HDMI, USB 3.0 |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | 40-pin header |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | I2C, UART, SPI |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | 3.3 V only |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |
