PYTHON = python3

main: complete

rkbin:
	git clone git@github.com:RKLins/rkbin.git rkbin

linaro_toolchain:
	- $(PYTHON) scripts/clone_linaro_toolchain.py

rkflashkit:
	- $(PYTHON) scripts/clone_rkflashkit.sh

preloader: rkbin
	$(PYTHON) scripts/make_preloader.py

uboot: linaro_toolchain rkbin
	$(PYTHON) scripts/make_uboot.py

complete: preloader uboot
