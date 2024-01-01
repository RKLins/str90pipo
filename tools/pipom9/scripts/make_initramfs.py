#!/usr/bin/python3

import os
import pathlib
import rockchip_environment
import tired.command
import tired.fs
import tired.logging


HERE = pathlib.Path(__file__).resolve().parent
RKBIN = HERE.parent / "rkbin"
INITRD_DESTINATION_DIR = HERE.parent / "initrd"
INITRD_OUT_FILE_PATH = HERE.parent / "initrd.img"


def clone_initramfs():
    if INITRD_DESTINATION_DIR.is_dir():
        tired.logging.info(f'Directory "{INITRD_DESTINATION_DIR}" already exists, skipping clone')

        return

    command = f"git clone https://github.com/RKLins/initrd.git {INITRD_DESTINATION_DIR}"
    tired.command.execute(command)


def build_initramfs():
    tired.command.execute(f"make -C {INITRD_DESTINATION_DIR}")


def main():
    rockchip_environment.update_env()
    clone_initramfs()
    build_initramfs()

    # Make sure the file is generated, and notify the user
    assert INITRD_OUT_FILE_PATH.is_file()
    tired.logging.info(f"Created initrd at {INITRD_OUT_FILE_PATH}")


if __name__ == "__main__":
    main()
