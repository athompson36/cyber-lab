# PineTime — Prototyping

- **Programming:** SWD (nRF52 standard); use J-Link or nRF DK. InfiniTime can be built with PlatformIO and flashed via openocd/J-Link.
- **Voltage:** 3.3 V only; no user GPIO breakout on production unit. DevKit may expose test points.
- **Do not** drive LCD/SPI or I2C pins to 5 V.
