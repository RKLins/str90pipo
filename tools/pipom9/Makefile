PYTHON = /usr/bin/python3
GIT = /usr/bin/git
BASH = /usr/bin/bash

main: complete

rkbins:
	$(GIT) clone git@github.com:RKLins/rkbin.git rkbin

linaro_toolchain:
	$(PYTHON) scripts/clone_linaro_toolchain.py

preloader: rkbin
	$(PYTHON) scripts/make_preloader.py

uboot: linaro_toolchain rkbin
	$(PYTHON) scripts/make_uboot.py

u-boot-sd.img: uboot
	cp u-boot/u-boot-sd.img .

trust: rkbin
	exit 0
	rkbin/tools/trust_merger rkbin/RKTRUST/

mkbootimg_tool/mkbootimg:
	$(PYTHON) scripts/make_boot_img.py

initrd.img:
	$(PYTHON) scripts/make_initramfs.py

Image:
	$(BASH) ./build.sh
	cp ../../arch/arm/boot/Image .
	echo Image -- done

config:
	$(BASH) ./configure_old.sh

boot.img: initrd.img mkbootimg_tool/mkbootimg
	mkbootimg_tool/mkbootimg --kernel Image --ramdisk initrd.img -o boot.img
	echo ./boot.img -- done

idbloader.img: preloader
	mv scripts/out/idbloader.img .
	echo idbloader.img -- done

parameter.img:
	$(BASH) scripts/make_parameter_img.sh
	mv scripts/parameter.img parameter.img
	echo parameter.img -- done

rootfs.ext4:
	$(PYTHON) scripts/rootfs.py
	mv scripts/rootfs.ext4 .

complete: idbloader.img u-boot-sd.img trust initrd.img boot.img rootfs.ext4

.PHONY: rkflashkit
