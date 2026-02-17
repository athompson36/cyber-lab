# platformio-lab: ESP32, Arduino, Teensy, Raspberry Pi, Pine64
# Build in container; flash from host.
# FROM ubuntu:22.04
ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    ninja-build \
    git \
    curl \
    wget \
    unzip \
    python3 \
    python3-pip \
    python3-venv \
    libusb-1.0-0 \
    udev \
    picocom \
    screen \
    gcc-arm-linux-gnueabihf \
    g++-arm-linux-gnueabihf \
    gcc-aarch64-linux-gnu \
    g++-aarch64-linux-gnu \
    && rm -rf /var/lib/apt/lists/*

# PlatformIO, ESP32/Arduino/Teensy/nRF52 toolchains (PIO installs per-platform on first build)
RUN pip3 install --no-cache-dir platformio

# ESP32: flash, merge_bin, image_info (T-Beam webflasher, CI, scripts)
RUN pip3 install --no-cache-dir esptool

# Serial scripting (config automation, repeater/room-server CLI)
RUN pip3 install --no-cache-dir pyserial

# Optional: Arduino CLI for non-PIO Arduino workflows
RUN pip3 install --no-cache-dir arduino-cli || true

WORKDIR /workspace

# Default: run shell so "docker run -it ..." works
CMD ["/bin/bash"]
