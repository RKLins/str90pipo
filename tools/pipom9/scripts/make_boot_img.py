#!/usr/bin/python3

"""
Builds "mkbootimg" tool, and builds the actual image

Dependencies:

- libcrypto (libssl)
"""

import os
import pathlib
import rockchip_environment
import tired.command
import tired.fs
import tired.logging


HERE = pathlib.Path(__file__).resolve().parent
RKBIN = HERE.parent / "rkbin"
MKBOOTIMG_PATH = HERE.parent / "mkbootimg_tool"
MKBOOTIMG_TOOL_OUT_PATH = MKBOOTIMG_PATH / "mkbootimg"


def build_mkbootimg():
    if not MKBOOTIMG_PATH.is_dir():
        command = f"git clone https://github.com/RKLins/rockchip-mkbootimg.git {MKBOOTIMG_PATH}"
        command = tired.command.execute(command)


    # `$nproc`
    rockchip_environment.update_env()

    os.chdir(MKBOOTIMG_PATH)
    tired.command.execute("make")
    tired.logging.info(f'Built "{MKBOOTIMG_TOOL_OUT_PATH.name}" at "{MKBOOTIMG_TOOL_OUT_PATH}"')


def main():
    if not MKBOOTIMG_TOOL_OUT_PATH.is_file():
        build_mkbootimg()


if __name__ == "__main__":
    main()
