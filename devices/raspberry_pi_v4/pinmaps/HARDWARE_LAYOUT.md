# Raspberry Pi 4 — Hardware Layout

**Board:** Raspberry Pi 4 Model B  
**SoC:** BCM2711 (Cortex-A72, 64-bit, 1.5–1.8 GHz), 1–8 GB LPDDR4

---

## 40-Pin GPIO Header

Same pinout as [raspberry_pi_zero](../../raspberry_pi_zero/pinmaps/HARDWARE_LAYOUT.md): 3V3 (1, 17), 5V (2, 4), I2C (3=SDA, 5=SCL), UART (8=TX, 10=RX), SPI (19,21,23,24,26), PWM (12,18,32,33), GND and GPIO0–27. All GPIO 3.3 V.

---

## Power

- 5 V via USB-C (recommended 3 A for full load). 3.3 V and 5 V on header as per table above.
