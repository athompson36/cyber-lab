# PineTime — Hardware Layout

**Board:** PINE64 PineTime (DevKit0)  
**SoC:** Nordic nRF52832 (Cortex-M4F, 64 MHz)

---

## nRF52832 Pin Assignment (PineTime)

| nRF Pins | Function | Notes |
|----------|----------|--------|
| P0.02 | SPI SCK | LCD |
| P0.03 | SPI MOSI | LCD |
| P0.04 | SPI MISO | |
| P0.05 | SPI CE# | SPI-NOR flash |
| P0.06 | I2C SDA | BMA421, HRS3300, touch |
| P0.07 | I2C SCL | |
| P0.08 | BMA421 INT | Accel interrupt |
| P0.12 | Charge indication | Input |
| P0.13 | Push button | Input |
| P0.14, P0.22, P0.23 | LCD backlight | Low / mid / high |
| P0.16 | Vibrator | Output |
| P0.18 | LCD RS | |
| P0.24 | 3V3 power control | Output |
| P0.25 | LCD CS | |
| P0.26 | LCD RESET | |
| P0.28 | Touch INT | Touchpad interrupt |
| P0.31 | Battery voltage | Analog |

---

## Power

- 3.3 V from internal PMU; battery voltage sense on P0.31. Charge indication on P0.12.

---

## References

- [Zephyr PineTime board](https://docs.zephyrproject.org/latest/boards/pine64/pinetime_devkit0/doc/index.html)
- [InfiniTime PinetimeStubWithNrf52DK](https://github.com/InfiniTimeOrg/InfiniTime/blob/main/doc/PinetimeStubWithNrf52DK.md)
- [PINE64 PineTime specs](https://www.pine64.org/pinetime/)
