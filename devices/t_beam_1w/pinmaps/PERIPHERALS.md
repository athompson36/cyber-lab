# T-Beam 1W — Available Peripherals

**Device:** LilyGO T-Beam 1W  
**Purpose:** List of all on-board peripherals with GPIO/bus assignments, drivers, and constraints.

---

## 1. LoRa Radio (SX1262 + 1W PA)

| Attribute | Value |
|-----------|--------|
| **Chip** | Semtech SX1262 |
| **Front-end** | 1W PA (external); TX must be limited to 22 dBm. |
| **Interface** | SPI (same bus as SD card). |
| **Pins** | NSS 15, RESET 3, DIO1 1, BUSY 38, MOSI 11, MISO 12, SCK 13. |
| **Control** | LDO_EN 40 (power for SX1262+PA), CTRL 21 (RXEN/LNA). |
| **LED** | TX activity: GPIO 18. |

**Constraints:**

- **GPIO 40** must be HIGH before any SX1262 init.
- **TX power:** firmware must cap at **22 dBm** (hardware safety).
- **PA ramp time:** set to **800 µs** (0x05); default 200 µs is too fast for 1W PA.
- RF switching: DIO2 internal to SX1262; GPIO 21 = RXEN (HIGH in RX).

**Drivers / config (this lab):**

- MeshCore: `CustomSX1262`, `CustomSX1262Wrapper`; build flags `SX126X_MAX_POWER=22`, `SX126X_PA_RAMP_TIME=0x05`.
- Meshtastic: variant `t-beam-1w`; same limits in variant/board code.

---

## 2. I2C Bus (Wire) — OLED + PMU

| Attribute | Value |
|-----------|--------|
| **Bus** | Single I2C (Wire); **no Wire1** on this board. |
| **Pins** | SDA 8, SCL 9. |
| **Devices** | OLED 0x3C, PMU 0x34 (optional). |

**OLED (SH1106):**

- Address: **0x3C**
- Resolution: **128×64**
- Driver: Adafruit SH110X or equivalent; use SH1106 (not SSD1306) in config.

**PMU (AXP2101):**

- Address: **0x34**
- **Optional:** Some cost-reduced boards do **not** populate AXP2101. I2C scan shows only 0x3C in that case.
- If present: battery voltage, charging, power paths. Use 2S range (6.0–8.4 V) for SoC.
- If absent: firmware should fall back to nominal 7.4 V (e.g. 7400 mV) and avoid NULL deref.

**Constraints:**

- Init I2C before accessing PMU or OLED.
- Do not assume dual I2C (T-Beam Supreme layout); this board is single bus only.

---

## 3. GNSS (L76K)

| Attribute | Value |
|-----------|--------|
| **Module** | Quectel L76K or compatible. |
| **Interface** | UART. |
| **Pins** | ESP RX ← GNSS TX: **GPIO 5**; ESP TX → GNSS RX: **GPIO 6**. |
| **Control** | Enable/Wake: **GPIO 16**. PPS (optional): **GPIO 7**. |
| **Baud** | **9600**. |

**Constraints:**

- Some firmware uses `PERSISTANT_GPS=1` and `ENV_SKIP_GPS_DETECT=1` to avoid timeout on slower cold start.
- PPS is optional; 7 is input from GNSS 1PPS.

---

## 4. Display (SH1106 OLED)

| Attribute | Value |
|-----------|--------|
| **Driver** | SH1106 (not SSD1306). |
| **Interface** | I2C, address **0x3C**. |
| **Resolution** | 128×64. |
| **Pins** | Shared with I2C (8, 9). |

**Constraints:**

- Boot/splash timing: use timer from UI/display init, not from power-on `millis()`, so splash is visible.

---

## 5. Buttons

| Button | GPIO | Notes |
|--------|------|--------|
| **USER_BTN** | 0 | Button 1; also BOOT for flashing. Internal pull-up. |
| **USER_BTN2** | 17 | Button 2. |

**Strapping:** GPIO 0 is strapping (boot mode); avoid driving at boot.

---

## 6. LED

| Role | GPIO | Polarity |
|------|------|----------|
| **TX / status** | 18 | HIGH = ON (LED_STATE_ON = 1). |

---

## 7. Fan

| Attribute | Value |
|-----------|--------|
| **Pin** | **GPIO 41**. |
| **Control** | Digital output. Recommended: ON after each TX, OFF after 5 s (saves power, reduces noise). |

---

## 8. Battery / Power Monitoring

| Attribute | Value |
|-----------|--------|
| **Chemistry** | 2S LiPo, 7.4 V nominal (6.0–8.4 V range). |
| **ADC (Meshtastic)** | GPIO 4, ADC1; multiplier ~2.9333; 30 samples. |
| **NTC (Meshtastic)** | GPIO 14 (temperature). |
| **PMU (optional)** | AXP2101 on I2C 0x34; if absent, use firmware fallback (e.g. 7400 mV). |

**Firmware:**

- `BATTERY_MIN_MILLIVOLTS=6000`, `BATTERY_MAX_MILLIVOLTS=8400`, `BATTERY_SERIES_CELLS=2` for 2S.

---

## 9. SD Card (Optional)

| Attribute | Value |
|-----------|--------|
| **Interface** | Shared SPI (MOSI 11, MISO 12, SCK 13). |
| **CS** | **GPIO 10**. |

Not all firmware enables SD; check build flags and wiring.

---

## 10. RTC / 32 kHz Crystal

| Attribute | Value |
|-----------|--------|
| **Crystal** | 32768 Hz present (HAS_32768HZ = 1 in some variants). |

Used for low-power RTC; no extra GPIO.

---

## 11. USB (ESP32-S3)

| Attribute | Value |
|-----------|--------|
| **Pins** | GPIO 19/20 (USB Serial/JTAG) or 45/46 (native USB); board uses USB for serial/flashing. |

Do not use 45/46 as GPIO when USB is active.

---

## Summary Table (Peripheral → GPIOs)

| Peripheral | GPIOs / bus | Notes |
|------------|-------------|--------|
| SX1262 + PA | 15,3,1,38,11,12,13,40,21,18 | 40 HIGH before init; 22 dBm max; 800 µs ramp |
| I2C (OLED, PMU) | 8, 9 | Single bus; 0x3C, 0x34 (PMU optional) |
| GNSS | 5,6,16,7 | UART 9600; 7 = PPS |
| Buttons | 0, 17 | 0 = BOOT strapping |
| LED | 18 | HIGH = ON |
| Fan | 41 | Post-TX 5 s recommended |
| Battery ADC / NTC | 4, 14 | 2S range 6.0–8.4 V |
| SD | 10 (+ SPI 11,12,13) | Optional |
