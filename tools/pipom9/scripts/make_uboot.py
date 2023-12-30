#!/usr/bin/python3

from . import rockchip_environment
import os
import pathlib
import tired.command
import tired.fs
import tired.logging


HERE = pathlib.Path(__file__).resolve().parent
RKBIN = HERE.parent / "rkbin"
UBOOT = HERE.parent / "u-boot-rockchip"


def main():
    if not UBOOT.is_dir():
        tired.command.execute(f"git clone https://github.com/rockchip-linux/u-boot.git {UBOOT}")
    else:
        tired.logging.info(f"{UBOOT.name} repository is already present, skipping")


if __name__ == "__main__":
    main()
