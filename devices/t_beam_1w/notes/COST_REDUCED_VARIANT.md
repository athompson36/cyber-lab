# T-Beam 1W — Cost-Reduced Variant (No AXP2101)

Some T-Beam 1W boards ship without the **AXP2101 PMU** populated (cost-reduced). The I2C bus at address 0x34 is empty; only the OLED at 0x3C responds.

## What changes

| Area | Standard board | Cost-reduced |
|------|---------------|--------------|
| PMU (AXP2101) | Present at I2C 0x34 | **Missing** |
| Battery voltage read | Via AXP2101 ADC | Not available; use fallback |
| Charging control | Via AXP2101 | Not available (charge IC may be separate or absent) |
| Power rail control | AXP2101 LDO/DCDC | Direct LDO on board, always on |

## Firmware requirements

All firmwares (MeshCore, Meshtastic, custom) must:

1. **NULL-check the PMU object** before any read/write. No NULL dereference if AXP2101 is absent.
2. **Fall back to nominal 2S voltage** (`7400 mV`) when PMU battery voltage returns 0 or init fails.
3. **Use 2S battery range** for UI: min 6000 mV, max 8400 mV, 2 cells in series.
4. **Skip PMU config calls** if init fails (don't retry in a loop or crash).

## Detection

```cpp
// I2C scan: if 0x34 not found, PMU is absent
Wire.beginTransmission(0x34);
bool hasPmu = (Wire.endTransmission() == 0);
```

## See also

- [shared/t_beam_1w/RF_PA_FAN_PMU.md](../../../shared/t_beam_1w/RF_PA_FAN_PMU.md) — canonical RF, PA, fan, PMU rules (section 3).
- T-BEAM-1W-FIXES.md in the MeshCore firmware repo — original fix notes.
