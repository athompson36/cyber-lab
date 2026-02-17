# Raspberry Pi 4 — SDKs & Tools

**Device:** Raspberry Pi 4 Model B  
**Container:** platformio-lab (cross-compile)  
**Current projects:** Pi digital mixer (3), sensor dashboard (5), media player (6), access control (7), effects rack (9).

---

## Build (in container)

| Tool / SDK | Purpose |
|------------|--------|
| **gcc-aarch64-linux-gnu** | 64-bit ARM kernel/userspace. |
| **Kernel** | raspberrypi/linux; `ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-`. |
| **Rootfs** | Buildroot (`raspberrypi4_64_defconfig`) or Yocto (meta-raspberrypi). |

---

## Deploy (host or Pi)

- Copy kernel/rootfs to SD; or use Raspberry Pi Imager, Armbian, etc.  
- Audio/DSP (mixer, effects) typically run on the Pi at runtime; build app with aarch64 in container.

---

## Docker dependencies (platformio-lab)

- gcc-aarch64-linux-gnu, g++-aarch64-linux-gnu, make, cmake, ninja, git, wget, unzip.

See [docker/TOOLS_AND_SDK.md](../../../docker/TOOLS_AND_SDK.md).
