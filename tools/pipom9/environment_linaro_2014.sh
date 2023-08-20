# Environment for building Linux for Pipo M9, RK3188-based platform

USE_CCACHE="1"

export ARCH=arm
export SRCARCH=arm
export INSTALL_MOD_PATH=./modules
export INSTALL_PATH=./install
# export MAKEFLAGS='--jobs=4'
export ENV_HERE_QUEUE_DIR=/home/dm/Documents/CODE-PipoM9RockchipLinux

echo home linaro 2014
. home_linux_common.sh
mkdir -p modules
export __LINARO_TOOLCHAIN_PATH="$(realpath linaro_toolchain)/arm-cortex_a9-linux-gnueabihf-linaro_4.9.3-2014.12"
export PATH=$__LINARO_TOOLCHAIN_PATH/bin:$PATH
export ARCH=arm
# export SUBARCH=arm


# Use ccache to improve build time
if [ -z ${USE_CCACHE} ] ; then
	echo  using ccache
	export CROSS_COMPILE="ccache $__LINARO_TOOLCHAIN_PATH/bin/arm-eabi-"
else
	export CROSS_COMPILE="$__LINARO_TOOLCHAIN_PATH/bin/arm-eabi-"
fi

# export CROSS_COMPILE=$__LINARO_TOOLCHAIN_PATH/bin/
export INSTALL_MOD_PATH=./modules
export INSTALL_PATH=./install
