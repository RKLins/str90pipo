#!/usr/bin/python3

import os
import pathlib
import shutil
import tired.command
import tired.fs


HERE = pathlib.Path(__file__).resolve().parent
RK3188_DDR = HERE / ".." / "rkbin" / "bin" / "r31" / "rk3188_ddr_v2.00.bin"
RKBIN = HERE.parent / "rkbin"
MKIMAGE = RKBIN / "tools" / "mkimage"
MINILOADER = tired.fs.find_unique("rk3188_miniloader_v2.00.bin", RKBIN)
DDR = tired.fs.find_unique("rk3188_ddr_v2.00.bin", RKBIN)
OUT = HERE / "out"
MINILOADER_OUT = OUT / MINILOADER.name
LOADER_OUT = OUT / "idbloader.img"
DDR_OUT = OUT / DDR.name


def main():
    try:
        os.mkdir(OUT)
    except FileExistsError as e:
        pass

    shutil.copy(MINILOADER, MINILOADER_OUT)
    shutil.copy(DDR, DDR_OUT)
    command = f"{MKIMAGE} -n rk3188 -T rksd -d {DDR_OUT} {LOADER_OUT}"
    tired.command.execute(command)
    os.system(f"cat {MINILOADER_OUT} >> {LOADER_OUT}")
    tired.logging.info("Output file", str(LOADER_OUT))
    os.remove(MINILOADER_OUT)
    os.remove(DDR_OUT)


if __name__ == "__main__":
    main()
