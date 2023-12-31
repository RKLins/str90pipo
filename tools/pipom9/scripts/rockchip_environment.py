#!/usr/bin/python3

import os
import pathlib
import tired.command
import tired.fs
import tired.logging


HERE = pathlib.Path(__file__).resolve().parent
IS_PATH_UPDATED = False
LINARO_TOOLCHAIN = (HERE.parent / "linaro_toolchain" / "arm-cortex_a9-linux-gnueabihf-linaro_4.9.3-2014.12").resolve()
SHELL_EXECUTABLE = "bash"
SHOULD_SET_NPROC = True


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
        os.environ["PS1"]

    should_use_ccache = os.getenv("USE_CCACHE", None)

    if should_use_ccache:
        setenv("CROSS_COMPILE", f"ccache {LINARO_TOOLCHAIN}/bin/arm-eabi-")
    else:
        setenv("CROSS_COMPILE", f"{LINARO_TOOLCHAIN}/bin/arm-eabi-")


if __name__ == "__main__":
    update_env()
    tired.logging.info("Entering virtual environment")
    os.system(SHELL_EXECUTABLE)
    tired.logging.info("Exited virtual environment")

