# Raspberry Pi Zero 2 W — Peripherals

| Peripheral | Pins | Notes |
|------------|------|--------|
| **I2C** | GPIO2 (SDA), GPIO3 (SCL); 3V3, GND | 1.8 kΩ pull-up typical; 400 kHz capable. ID EEPROM: 27 (ID_SD), 28 (ID_SC). |
| **UART** | GPIO14 (TXD), GPIO15 (RXD) | 3.3 V; primary serial console (often enabled for serial shell). |
| **SPI** | GPIO9 (MISO), GPIO10 (MOSI), GPIO11 (SCLK), GPIO8 (CE0), GPIO7 (CE1) | 3.3 V; SPI0. |
| **PWM** | GPIO12, GPIO18 (PWM0); GPIO13 (PWM1) | Software PWM available on other GPIOs. |
| **GPIO** | GPIO0–27 (excluding dedicated I2C/UART/SPI) | All 3.3 V; not 5 V tolerant. |

---

## Constraints

- **Voltage:** All GPIO 3.3 V; maximum current per pin ~16 mA, total limit per spec.
- **No 5 V input** on GPIO; level-shift if connecting 5 V logic.
