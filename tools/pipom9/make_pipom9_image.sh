#!/bin/bash

ZIMAGE_PATH="./../../arch/arm/boot/zImage"
DATE=$(date +%Y%m%d%H%M | tr -d \\n)

mkbootimg --kernel ${ZIMAGE_PATH} --ramdisk initrd.img --output str90-image-${DATE}.bin
