# Raspberry Pi Zero 2 W — Prototyping

- **GPIO:** 3.3 V only; not 5 V tolerant. Use level shifters for 5 V logic.
- **Header:** 40-pin 2×20, 0.1" (2.54 mm); HAT-compatible; some HATs may need spacers (Zero is thin).
- **Power:** 5 V via micro USB (typically 1.2 A recommended); do not backfeed 5 V and USB at same time without care.
- **Free pins:** Any GPIO not used by your image for I2C/UART/SPI can be used; avoid ID_SD/ID_SC if using HAT EEPROM.
