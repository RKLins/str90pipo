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


def update_env():
    tired.logging.info("setting environment variable ARCH")
    os.environ["ARCH"] = "arm"
    tired.logging.info("setting environment variable SRCARCH")
    os.environ["SRCARCH"] = "arm"
    tired.logging.info("setting environment variable INSTALL_MOD_PATH")
    os.environ["INSTALL_MOD_PATH"] = "./modules"
    tired.logging.info("setting environment variable INSTALL_PATH")
    os.environ["INSTALL_PATH"] = "./install"
    tired.logging.info("setting environment variable PATH")
    os.environ["PATH"] = os.environ["PATH"] + ":" + str(LINARO_TOOLCHAIN)

    if SHELL_EXECUTABLE == "bash":
        os.environ["PS1"]

    should_use_ccache = os.getenv("USE_CCACHE", None)

    if should_use_ccache:
        tired.logging.info("setting environment variable CROSS_COMPILE, using ccache")
        os.environ["CROSS_COMPILE"] = f"ccache {LINARO_TOOLCHAIN}/bin/arm-eabi-"
    else:
        tired.logging.info("setting environment variable CROSS_COMPILE, NOT using ccache")
        os.environ["CROSS_COMPILE"] = f"{LINARO_TOOLCHAIN}/bin/arm-eabi-"


if __name__ == "__main__":
    update_env()
    tired.logging.info("Entering virtual environment")
    os.system(SHELL_EXECUTABLE)
    tired.logging.info("Exited virtual environment")

