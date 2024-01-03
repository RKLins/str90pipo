PYTHON = /usr/bin/python3
GIT = /usr/bin/git
BASH = /usr/bin/bash
MKBOOTIMG = mkbootimg_tool/mkbootimg
RKDEVELOPTOOL = rkbin/tools/rkdeveloptool

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

$(MKBOOTIMG):
	$(PYTHON) scripts/make_boot_img.py

initrd.img:
	$(PYTHON) scripts/make_initramfs.py

Image:
	$(BASH) ./build.sh
	cp ../../arch/arm/boot/Image .
	echo Image -- done

# The old (working) way of preparing the image
bootimage: Image $(MKBOOTIMG)
	$(MKBOOTIMG) --kernel Image --ramdisk initrd.img --output str90-image-$$(date +%Y%m%d%H%M | tr -d \\n).bin

zImage:
	$(BASH) ./scripts/build_zimage.sh

bootzimage: zImage $(MKBOOTIMG) initrd.img
	$(MKBOOTIMG) --kernel zImage --ramdisk initrd.img --output str90-zimage-$$(date +%Y%m%d%H%M | tr -d \\n).bin

flash_bootzimage: $(RKDEVELOPTOOL)
	sudo RKDEVELOPTOOL=$(RKDEVELOPTOOL) scripts/flash_bootzimage.sh

config:
	$(BASH) ./configure_old.sh

boot.img: initrd.img mkbootimg_tool/mkbootimg Image
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
	echo rootfs.ext4 -- done

rkcrc:
	-$(GIT) clone https://github.com/RKLins/rkflashtool.git rkflashtool
	$(MAKE) -C rkflashtool
	cd rkflashtool \
		&& cp -f rkflashtool rkcrc rkunpack rkunsign ~/bin

parameter.img:
	cd scripts \
		&& $(BASH) make_parameter_img.sh
	cp scripts/parameter.img parameter.img


complete: idbloader.img u-boot-sd.img trust parameter.img initrd.img boot.img rootfs.ext4

.PHONY: rkflashkit
