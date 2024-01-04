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
import tired.env
import tired.fs
import tired.logging
import tired.ui


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


def clone_kitcat_uboot_google_toolchain():
    toolchain_dir = HERE.parent / "toolchain-arm-eabi-4.6"

    if not toolchain_dir.is_dir():
        tired.command.execute(f'git clone https://github.com/RKLins/linaro-toolchain-uboot.git "{toolchain_dir}"')
    else:
        tired.logging.info(f'The toolchain directory "{toolchain_dir}" is already present, assuming the toolchain is already installed, skipping')


def clone_radxa_uboot():
    # Clone from git, if haven't yet
    if not UBOOT.is_dir():
        tired.command.execute(f"git clone -b u-boot-rk3188-sdcard https://github.com/RKLins/u-boot-rockchip.git {UBOOT}")
    else:
        tired.logging.info(f"{UBOOT.name} repository is already present, skipping")


def build_radxa_uboot_sd():
    tired.logging.info("Building Radxa U-Boot (SD)")
    tired.logging.info(f"Changing PWD: ${UBOOT}")
    os.chdir(UBOOT)
    tired.command.execute("git checkout u-boot-rk3188-sdcard")
    tired.command.execute(f"make rk30xx")
    tired.command.execute(f"./pack-sd.sh")


def build_radxa_uboot_nand():
    tired.logging.info("Building Radxa U-Boot (NAND)")
    tired.logging.info(f"Changing PWD: ${UBOOT}")
    os.chdir(UBOOT)
    tired.command.execute("git checkout u-boot-rk3188")
    tired.command.execute(f"make rk30xx")


def pack_uboot():
    """
    Pack U-Boot when using idbloader
    https://opensource.rock-chips.com/wiki_Boot_option (search for "When using
    idbLoader")
    """
    tired.logging.info("Packing U-Boot")
    loaderimage = RKBIN / "tools" / "loaderimage"
    command = f'{loaderimage} --pack --uboot "{UBOOT_OUT}" "{UBOOT_PACKED_OUT}" "{SYS_TEXT_BASE}"'
    tired.command.execute(command)


def main(make_for_sd=True):
    # Clone
    clone_radxa_uboot()

    # Ensure the proper toolchain is installed
    clone_kitcat_uboot_google_toolchain()

    # Update necessary environment variables
    rockchip_environment.update_env_uboot()

    # Execute
    if tired.env.try_get_env("CONFIG_PIPO_UBOOT_SD") is None:
        tired.ui.select_callback({
            "Build Radxa U-Boot for SD card": build_radxa_uboot_sd,
            "Build Radxa U-Boot for NAND": build_radxa_uboot_nand,
        })
    else:
        build_radxa_uboot_sd()

    # Pack u-boot
    should_pack_uboot = tired.env.try_get_env("CONFIG_PIPO_UBOOT_PACK_IDBLOADER", type_=bool)

    if should_pack_uboot is None and tired.ui.select_yn("Pack U-Boot with idbloader?"):
        pack_uboot()


if __name__ == "__main__":
    main()
