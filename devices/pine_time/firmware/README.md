# PineTime — Firmware Repos

**Full index:** [FIRMWARE_INDEX.md](../../../FIRMWARE_INDEX.md#pine_time-pine64-pinetime)

| Firmware / project | Repo | Notes |
|--------------------|------|--------|
| **InfiniTime** | [InfiniTimeOrg/InfiniTime](https://github.com/InfiniTimeOrg/InfiniTime) | FreeRTOS; PlatformIO/CMake. |
| **Zephyr** (official) | [Zephyr pinetime_devkit0](https://docs.zephyrproject.org/latest/boards/pine64/pinetime_devkit0/doc/index.html) | Board: `pinetime_devkit0`. |
| **nRF Connect SDK** | [nrfconnect/sdk-nrf](https://github.com/nrfconnect/sdk-nrf) | Zephyr-based; PineTime support. |
| **Hypnos** (Zephyr) | [albsod/pinetime-hypnos](https://github.com/albsod/pinetime-hypnos) | Zephyr; ~1 week battery, LVGL. |
| **wasp-os** (MicroPython) | [wasp-os/wasp-os](https://github.com/wasp-os/wasp-os) | Switchable with InfiniTime. |
| **wasp-os bootloader** | [wasp-os/wasp-bootloader](https://github.com/wasp-os/wasp-bootloader) | OTA. |
| **wasp-reloader** | [wasp-os/wasp-reloader](https://github.com/wasp-os/wasp-reloader) | Switch InfiniTime ↔ wasp-os. |
| **pinotime** (MicroPython) | [MrPicklePinosaur/pinotime](https://github.com/MrPicklePinosaur/pinotime) | MicroPython dev env. |
| PINE64 PineTime | [pine64.org/pinetime](https://www.pine64.org/pinetime/) | Specs, links. |

Build in lab: **PlatformIO** (platform `nordicnrf52`, board e.g. `pinetime_devkit0`) or **Zephyr** in **platformio-lab**.
