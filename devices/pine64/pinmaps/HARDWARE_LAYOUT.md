# Pine A64 — Hardware Layout

**Board:** Pine A64 / Pine64  
**SoC:** Allwinner A64 (Cortex-A53, 64-bit)

---

## Expansion Headers (Euler)

Pine A64 uses two 28-pin (2×14) headers; pinout is SoC-specific (A64 GPIO banks). Refer to [PINE64 wiki](https://wiki.pine64.org/wiki/Pine_A64) and [schematic](https://files.pine64.org/doc/Pine%20A64%20Schematic.pdf) for exact GPIO mapping. Typical: 3.3 V, GND, GPIOs, I2C, UART, SPI. **Do not apply 5 V to GPIO.**

---

## Power

- 5 V input (barrel or micro USB); 3.3 V on expansion for peripherals.
