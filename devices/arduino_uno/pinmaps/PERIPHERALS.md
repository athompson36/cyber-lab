# Arduino Uno R3 — Peripherals

| Peripheral | Pins | Notes |
|------------|------|--------|
| **UART** | D0 (RX), D1 (TX) | 0/1 shared with USB serial; avoid for I/O when using Serial. |
| **I2C** | A4 (SDA), A5 (SCL) | Internal pull-ups; 5 V. |
| **SPI** | D10 (SS), D11 (MOSI), D12 (MISO), D13 (SCK) | D13 = built-in LED. |
| **PWM** | D3, D5, D6, D9, D10, D11 | 8-bit; 490 Hz or 980 Hz (timer-dependent). |
| **Analog** | A0–A5 | 10-bit ADC; 5 V ref default. |
| **External interrupt** | D2 (INT0), D3 (INT1) | |

All digital I/O 5 V; max 40 mA per pin. Do not exceed 5 V on any pin.
