#!/usr/bin/python3

import os
import pathlib
import tired.command
import tired.fs
import tired.logging
import tired.ui


HERE = pathlib.Path(__file__).resolve().parent
IS_PATH_UPDATED = False
LINARO_TOOLCHAIN = (HERE.parent / "linaro_toolchain" / "arm-cortex_a9-linux-gnueabihf-linaro_4.9.3-2014.12").resolve()
SHELL_EXECUTABLE = "bash"
SHOULD_SET_NPROC = True
RADXA_RECOMMENDED_UBOOT_TOOLCHAIN = (HERE.parent / "toolchain-arm-eabi-4.6")


def get_nproc():
    return 20


def setenv(variable, value):
    tired.logging.info(f'Setting environment variable "{variable}"="{value}"')
    os.environ[str(variable)] = str(value)


def update_env():
    setenv("ARCH", "arm")
    setenv("SRCARCH", "arm")
    setenv("INSTALL_MOD_PATH", "./modules")
    setenv("INSTALL_PATH", "./install")
    setenv("PATH", os.environ["PATH"] + ":" + str(LINARO_TOOLCHAIN))

    if SHOULD_SET_NPROC:
        setenv("MAKEFLAGS", get_nproc())

    if SHELL_EXECUTABLE == "bash":
        os.environ["PS1"] = "(rockchip environment) " + os.environ["PS1"]

    should_use_ccache = os.getenv("USE_CCACHE", None)

    if should_use_ccache:
        setenv("CROSS_COMPILE", f"ccache {LINARO_TOOLCHAIN}/bin/arm-eabi-")
    else:
        setenv("CROSS_COMPILE", f"{LINARO_TOOLCHAIN}/bin/arm-eabi-")


def update_env_uboot():
    """
    The upstream U-Boot does not support RK3188. Rockchip recommends using
    Radxa U-Boot https://wiki.radxa.com/Rock/U-Boot. Radxa U-Boot recommends
    using a particular version of GCC toolchain.
    """
    tired.logging.info(f'Setting up uboot env with "{RADXA_RECOMMENDED_UBOOT_TOOLCHAIN}" toolchain')
    setenv("ARCH", "arm")
    setenv("SRCARCH", "arm")
    setenv("INSTALL_MOD_PATH", "./modules")
    setenv("INSTALL_PATH", "./install")
    setenv("PATH", os.environ["PATH"] + ":" + str(RADXA_RECOMMENDED_UBOOT_TOOLCHAIN))

    if SHOULD_SET_NPROC:
        setenv("MAKEFLAGS", get_nproc())

    if SHELL_EXECUTABLE == "bash":
        os.environ["PS1"] = "(radxa rockchip environment) " + os.environ["PS1"]

    should_use_ccache = os.getenv("USE_CCACHE", None)

    if should_use_ccache:
        setenv("CROSS_COMPILE", f"ccache {RADXA_RECOMMENDED_UBOOT_TOOLCHAIN}/bin/arm-eabi-")
    else:
        setenv("CROSS_COMPILE", f"{RADXA_RECOMMENDED_UBOOT_TOOLCHAIN}/bin/arm-eabi-")


if __name__ == "__main__":
    profiles = {
        "Linaro 4.9": update_env,
        "GCC 4.6 (Radxa U-Boot-compatible)": update_env_uboot,
    }
    tired.ui.select_callback(profiles, "Select profile")
    tired.logging.info("Entering virtual environment")
    os.system(SHELL_EXECUTABLE)
    tired.logging.info("Exited virtual environment")

