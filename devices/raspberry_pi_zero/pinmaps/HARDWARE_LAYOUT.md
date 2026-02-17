# Raspberry Pi Zero 2 W — Hardware Layout

**Board:** Raspberry Pi Zero 2 W  
**SoC:** BCM2710A1 (Cortex-A53, 64-bit, 1 GHz), 512 MB LPDDR2

---

## 40-Pin GPIO Header (HAT-compatible)

Pinout matches Raspberry Pi 4 / Pi 5 40-pin layout.

| Pin | BCM | Function | Pin | BCM | Function |
|-----|-----|----------|-----|-----|----------|
| 1 | 3V3 | Power | 2 | 5V | Power |
| 3 | GPIO2 | I2C SDA1 | 4 | 5V | Power |
| 5 | GPIO3 | I2C SCL1 | 6 | GND | Ground |
| 7 | GPIO4 | GPCLK0 | 8 | GPIO14 | UART TXD |
| 9 | GND | Ground | 10 | GPIO15 | UART RXD |
| 11 | GPIO17 | GPIO | 12 | GPIO18 | PWM0 |
| 13 | GPIO27 | GPIO | 14 | GND | Ground |
| 15 | GPIO22 | GPIO | 16 | GPIO23 | GPIO |
| 17 | 3V3 | Power | 18 | GPIO24 | GPIO |
| 19 | GPIO10 | SPI MOSI | 20 | GND | Ground |
| 21 | GPIO9 | SPI MISO | 22 | GPIO25 | GPIO |
| 23 | GPIO11 | SPI SCLK | 24 | GPIO8 | SPI CE0 |
| 25 | GND | Ground | 26 | GPIO7 | SPI CE1 |
| 27 | ID_SD | I2C ID EEPROM | 28 | ID_SC | I2C ID EEPROM |
| 29 | GPIO5 | GPIO | 30 | GND | Ground |
| 31 | GPIO6 | GPIO | 32 | GPIO12 | PWM0 |
| 33 | GPIO13 | PWM1 | 34 | GND | Ground |
| 35 | GPIO19 | SPI MISO | 36 | GPIO16 | GPIO |
| 37 | GPIO26 | GPIO | 38 | GPIO20 | SPI MOSI |
| 39 | GND | Ground | 40 | GPIO21 | SPI SCLK |

---

## Power

- **3.3 V** (pins 1, 17): GPIO and peripherals; do not exceed 3.3 V on any GPIO.
- **5 V** (pins 2, 4): Input for board power (micro USB or 5 V pin); output on 5 V pins when powered.
- **GND**: Pins 6, 9, 14, 20, 25, 30, 34, 39.

---

## Block Diagram

```
micro USB (power) ──► PMIC ──► 3.3 V / 1.8 V ──► BCM2710A1, WiFi/BT, GPIO
microSD ─────────────────────────────────────► SoC (boot + rootfs)
40-pin header ────────────────────────────────► GPIO / I2C / UART / SPI / PWM
Mini HDMI ───────────────────────────────────► Display
```

---

## References

- [Raspberry Pi Zero 2 W Product Brief](https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf)
- [Pinout (pinout.xyz)](https://pinout.xyz/pinout/pin1_3v3_power)
- [BCM2835 ARM Peripherals](https://datasheets.raspberrypi.com/bcm2835/bcm2835-peripherals.pdf) (register-level; BCM2710 is compatible for GPIO view)
