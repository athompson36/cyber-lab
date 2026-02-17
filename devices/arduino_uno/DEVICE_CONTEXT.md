# Device Context — Arduino Uno R3

**Device ID:** `arduino_uno`  
**Board:** Arduino Uno Rev3 (ATmega328P)  
**Lab contract:** `firmware/` · `configs/` · `pinmaps/` · `notes/`

---

## Summary

Arduino Uno R3 uses ATmega328P (8-bit AVR, 16 MHz), 32 KB flash, 2 KB SRAM. 14 digital I/O (6 PWM), 6 analog inputs; I2C and SPI on dedicated pins. Build with PlatformIO (atmelavr) or Arduino CLI in container.

---

## Hardware at a Glance

| Item | Detail |
|------|--------|
| **MCU** | ATmega328P (8-bit AVR, 16 MHz), 32 KB flash, 2 KB SRAM, 1 KB EEPROM |
| **Digital** | 14 pins (D0–D13); 6 PWM (3, 5, 6, 9, 10, 11); 40 mA max per pin |
| **Analog** | 6 inputs (A0–A5); A4/A5 are I2C (SDA/SCL) |
| **Voltage** | 5 V logic; not 3.3 V native (use level shifter for 3.3 V systems) |

---

## Context Files

| File | Description |
|------|-------------|
| [pinmaps/HARDWARE_LAYOUT.md](pinmaps/HARDWARE_LAYOUT.md) | Pinout table, power |
| [pinmaps/PERIPHERALS.md](pinmaps/PERIPHERALS.md) | UART, I2C, SPI, PWM |
| [notes/PROTOTYPING.md](notes/PROTOTYPING.md) | 5 V, current limits |
| [firmware/README.md](firmware/README.md) | Arduino core, PlatformIO, firmware repos |
