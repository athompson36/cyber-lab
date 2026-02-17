# Device Context — PineTime

**Device ID:** `pine_time`  
**Board:** PINE64 PineTime (nRF52832, smartwatch)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

PineTime is an open smartwatch: Nordic nRF52832 (Cortex-M4F, 64 MHz, 64 KB RAM, 512 KB flash), 1.3" display, SPI NOR, I2C sensors (BMA421, HRS3300), touch. Runs InfiniTime, Zephyr, or other embedded firmware. Build with PlatformIO (nordicnrf52) or Zephyr/arm-none-eabi in container.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | nRF52832 (Cortex-M4F, 64 MHz), 64 KB SRAM, 512 KB flash |
| **Display** | 1.3" 240×240, SPI; LCD driver on P0.02–P0.05, P0.18, P0.25, P0.26 |
| **Storage** | 4 MB SPI NOR (P0.05 CE#) |
| **Sensors** | BMA421 (accel), HRS3300 (HR), I2C on P0.06 (SDA), P0.07 (SCL) |
| **Input** | Touch (P0.28 INT), button (P0.13) |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | nRF52832 pinout, display, sensors |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | SPI, I2C, GPIO list |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | SWD, 3.3 V |
| [firmware/README.md](firmware/README.md) | InfiniTime, Zephyr, other firmware repos |
