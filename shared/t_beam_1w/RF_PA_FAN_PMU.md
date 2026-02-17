# T-Beam 1W — RF, PA, Fan, PMU (Shared Rules)

**Device:** LilyGO T-Beam 1W (ESP32-S3 + SX1262 + 1W PA)  
**Purpose:** Canonical constraints for radio, power amplifier, cooling fan, and PMU. All firmwares (MeshCore, Meshtastic, custom) must follow these.

---

## 1. Radio (SX1262) and 1W PA

| Item | Value |
|------|--------|
| **Chip** | Semtech SX1262 |
| **Front-end** | 1W external PA; TX must be limited to **22 dBm** (hardware safety). |
| **Interface** | SPI (NSS 15, RESET 3, DIO1 1, BUSY 38, MOSI 11, MISO 12, SCK 13). |
| **Control** | **GPIO 40 (LDO_EN)** powers SX1262 + PA. **GPIO 21 (CTRL)** = RXEN/LNA. |

### Firmware requirements

1. **GPIO 40** must be driven **HIGH before** any SX1262/radio init (powers radio + PA LDO). Do not drive LOW during normal operation.
2. **TX power** must be capped at **22 dBm** in build flags and runtime; never exceed for 1W PA safety.
3. **PA ramp time** must be set to **800 µs** (0x05) in radio init; default 200 µs is too fast for 1W PA.
4. **Antenna:** Do not transmit without an antenna connected (RF damage risk).

### Build flags (typical)

- `SX126X_MAX_POWER=22`
- `SX126X_PA_RAMP_TIME=0x05` (800 µs)

### Init order

1. GPIO 40 (LDO_EN) → HIGH.  
2. GPIO 3 (RESET) → HIGH.  
3. I2C begin (if using OLED/PMU).  
4. SX1262 init (SPI, RESET, DIO1, BUSY, CTRL); set PA ramp 800 µs, cap TX 22 dBm.

---

## 2. Cooling Fan

| Item | Value |
|------|--------|
| **Pin** | **GPIO 41** (FAN_CTRL). |
| **Control** | Digital output. |

**Recommendation:** Turn fan ON after each TX burst; turn OFF after ~5 s to save power and reduce noise.

---

## 3. PMU (AXP2101)

| Item | Value |
|------|--------|
| **Chip** | AXP2101 (X-Powers). |
| **Interface** | I2C, address **0x34**. |
| **Bus** | Same I2C as OLED (SDA 8, SCL 9); **single bus only** (no Wire1). |

**Important:** Some cost-reduced boards do **not** populate AXP2101. I2C scan may show only 0x3C (OLED). Firmware must:

- Handle missing PMU (no NULL deref).
- Fall back to nominal 2S voltage (e.g. 7400 mV) when PMU is absent.
- Use 2S range (6.0–8.4 V) for battery UI and limits.

---

## 4. Power Tree (Summary)

- **GPIO 40** gates LDO power to SX1262 + 1W PA; must be HIGH before radio use.
- **USB-C 5 V** and **2S LiPo (7.4 V)** feed AXP2101 (if present) or direct 3.3 V LDO on cost-reduced boards.
- **Battery:** 2S LiPo, 6.0–8.4 V range; use `BATTERY_MIN_MILLIVOLTS=6000`, `BATTERY_MAX_MILLIVOLTS=8400`, `BATTERY_SERIES_CELLS=2` in firmware.

---

## 5. Do not

- Do not drive GPIO 40 LOW during normal operation (radio/PA lose power).
- Do not assign GPIO 0, 3, 40, 21 to unrelated peripherals (boot, reset, radio power, RF switch).
- Do not exceed 22 dBm TX or use PA ramp &lt; 800 µs.
- Do not assume a second I2C bus (Wire1) for OLED/PMU; this board has one bus.
- Do not assume AXP2101 is present; always handle missing PMU in code.
- Do not transmit without an antenna connected.

---

## References

- [devices/t_beam_1w/pinmaps/HARDWARE_LAYOUT.md](../../devices/t_beam_1w/pinmaps/HARDWARE_LAYOUT.md) — pinout and power tree.
- [devices/t_beam_1w/pinmaps/PERIPHERALS.md](../../devices/t_beam_1w/pinmaps/PERIPHERALS.md) — full peripheral list.
- [devices/t_beam_1w/notes/PROTOTYPING.md](../../devices/t_beam_1w/notes/PROTOTYPING.md) — free GPIOs and safety checklist.
- If using MeshCore clone: see `T-BEAM-1W-FIXES.md` in the firmware repo for known fixes.
