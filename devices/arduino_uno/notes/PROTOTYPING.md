# Arduino Uno R3 — Prototyping

- **Voltage:** 5 V logic; do not apply > 5 V to any I/O. For 3.3 V peripherals use level shifter.
- **Current:** 40 mA max per pin; 200 mA total from all pins combined recommended.
- **D0/D1:** Avoid using as GPIO when Serial (USB) is in use.
- **I2C:** A4/A5; add external pull-ups if bus is long or many devices.
