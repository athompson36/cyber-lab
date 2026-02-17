# Arduino Uno R3 — Hardware Layout

**Board:** Arduino Uno Rev3  
**MCU:** ATmega328P (16 MHz)

---

## Pinout Summary

| Pin | Function | Notes |
|-----|----------|--------|
| 0 | RX (serial) | Do not use for digital I/O when Serial used |
| 1 | TX (serial) | Do not use for digital I/O when Serial used |
| 2–3 | Digital; INT0, INT1 | External interrupts |
| 3, 5, 6, 9, 10, 11 | PWM | 8-bit PWM |
| 10–13 | SS, MOSI, MISO, SCK | SPI (D10 = SS) |
| 13 | Built-in LED | On-board LED |
| A0–A5 | Analog input | 10-bit ADC; A4 = SDA, A5 = SCL (I2C) |

---

## Power

- **5 V:** From USB or VIN (7–12 V recommended to regulator). 5 V pin output when powered.
- **3.3 V:** 3.3 V regulator output (50 mA max); GPIO are 5 V logic.
- **GND:** Multiple GND pins.

---

## References

- [Arduino Uno Rev3](https://docs.arduino.cc/hardware/uno-rev3)
- [Pinout (pinout.xyz)](https://pinout.xyz/pinout/arduino_uno_r3)
