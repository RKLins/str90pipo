#!/usr/bin/python3

"""
Implements U-Boot build instructions from:
- https://wiki.radxa.com/Rock/U-Boot
- https://opensource.rock-chips.com/wiki_Boot_option#U-Boot
"""

import os
import pathlib
import rockchip_environment
import tired.command
import tired.fs
import tired.logging


HERE = pathlib.Path(__file__).resolve().parent

# U-Boot repository
UBOOT = HERE.parent / "u-boot"

# Rockchip utility binaries
RKBIN = HERE.parent / "rkbin"

# Compiled U-Boot
UBOOT_OUT = UBOOT / "u-boot-sd.img"

# Packed U-Boot
UBOOT_PACKED_OUT = HERE / "uboot.img"

# RK3188 memory layout, flash (TODO: verify)
SYS_TEXT_BASE = "0x80000000"

def build_rockchip_uboot():
    # Change toolchain location
    cross_compile_command_argument = f"CROSS_COMPILE={os.getenv('CROSS_COMPILE')}"

    # Specify target
    target_command_argument = "rk3188"

    # Execute
    tired.logging.info(f"Changing PWD: ${UBOOT}")
    os.chdir(UBOOT)
    command = f"make.sh {cross_compile_command_argument} {target_command_argument}"
    tired.command.execute(command)


def clone_radxa_uboot():
    # Clone from git, if haven't yet
    if not UBOOT.is_dir():
        tired.command.execute(f"git clone -b u-boot-rk3188-sdcard https://github.com/RKLins/u-boot-rockchip.git {UBOOT}")
    else:
        tired.logging.info(f"{UBOOT.name} repository is already present, skipping")


def build_radxa_uboot():
    tired.logging.info("Building Radxa U-Boot")
    tired.logging.info(f"Changing PWD: ${UBOOT}")
    os.chdir(UBOOT)
    tired.command.execute(f"make rk30xx")
    tired.command.execute(f"./pack-sd.sh")


def pack_uboot():
    tired.logging.info("Packing U-Boot")
    loaderimage = RKBIN / "tools" / "loaderimage"
    command = f'{loaderimage} --pack --uboot "{UBOOT_OUT}" "{UBOOT_PACKED_OUT}" "{SYS_TEXT_BASE}"'
    tired.command.execute(command)


def main():
    # Clone
    clone_radxa_uboot()

    # Update necessary environment variables
    rockchip_environment.update_env()

    # Execute
    build_radxa_uboot()

    # Pack u-boot
    pack_uboot()


if __name__ == "__main__":
    main()
