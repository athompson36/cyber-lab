# Raspberry Pi Zero 2 W — Firmware & OS Repos

Pi Zero 2 W runs **Linux** (or other OS); "firmware" here means boot blobs, kernel, and rootfs.

**Full index:** [FIRMWARE_INDEX.md](../../../FIRMWARE_INDEX.md#raspberry_pi_zero-raspberry-pi-zero-2-w)

## Official / primary

| Repo | Description |
|------|-------------|
| [raspberrypi/firmware](https://github.com/raspberrypi/firmware) | Boot binaries, GPU firmware, drivers (install to `/boot` on SD). |
| [raspberrypi/linux](https://github.com/raspberrypi/linux) | Kernel source (BCM2710/BCM2835 family). |
| [raspberrypi/documentation](https://github.com/raspberrypi/documentation) | Official docs and guides. |

## OS / rootfs

| Repo / project | Description |
|----------------|-------------|
| [Raspberry Pi OS](https://www.raspberrypi.com/software/) | Official Debian-based OS (image or Imager). |
| [buildroot/buildroot](https://github.com/buildroot/buildroot) | Custom minimal Linux; `board/raspberrypi`, e.g. `raspberrypi0_2w_defconfig`. |
| [Yocto](https://www.yoctoproject.org/) | BSP: [meta-raspberrypi](https://git.yoctoproject.org/meta-raspberrypi). |

## Build in lab

- Cross-compile with **gcc-aarch64-linux-gnu** (64-bit) in **platformio-lab** (or dedicated ARM container).
- Kernel: use kernel build system; point `ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-`.
- Rootfs: Buildroot/Yocto output; copy to SD with boot partition from `raspberrypi/firmware`.
