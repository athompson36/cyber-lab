# Device Context — PinePhone

**Device ID:** `pine_phone`  
**Board:** PINE64 PinePhone (Allwinner A64, Linux smartphone)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

PinePhone is an open Linux smartphone: Allwinner A64 (or later variants), modem, display, battery. Runs mainline Linux, postmarketOS, Manjaro ARM, etc. Development typically via SSH or serial; expansion is limited compared to SBCs. Build with aarch64 cross-compiler for userspace and kernel.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **SoC** | Allwinner A64 (PinePhone 1.x) or A53-based SoC; varies by revision |
| **Form** | Smartphone; no standard GPIO header; USB-C, modem, display |
| **Storage** | eMMC, microSD |
| **OS** | postmarketOS, Manjaro ARM, Ubuntu Touch, others |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | Connectors, no general-purpose header |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | Modem, display, USB, I2C (internal) |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | Serial console, USB; no exposed GPIO |
| [firmware/README.md](firmware/README.md) | OS and firmware repos |
