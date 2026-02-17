# PineTime — Peripherals

| Peripheral | Pins | Notes |
|------------|------|--------|
| **SPI (LCD + NOR)** | P0.02 (SCK), P0.03 (MOSI), P0.04 (MISO), P0.05 (NOR CE#), P0.25 (LCD CS) | LCD and 4 MB NOR on same bus |
| **LCD control** | P0.26 (RESET), P0.18 (RS) | |
| **I2C** | P0.06 (SDA), P0.07 (SCL) | BMA421, HRS3300, touch controller |
| **Backlight** | P0.14, P0.22, P0.23 | 3-level backlight |
| **Vibrator** | P0.16 | |
| **Button** | P0.13 | |
| **Touch INT** | P0.28 | |
| **BMA421 INT** | P0.08 | |
| **Battery** | P0.31 (ADC), P0.12 (charge) | |
| **3V3 enable** | P0.24 | |

All 3.3 V. SWD for programming (standard nRF52 SWD pins).
