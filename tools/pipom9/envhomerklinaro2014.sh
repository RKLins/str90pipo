# Environment for building Linux for Pipo M9, RK3188-based platform

echo home linaro 2014
. home_linux_common.sh
mkdir -p modules
export __LINARO_TOOLCHAIN_PATH="/home/dm/Documents/CODE-PipoM9RockchipLinux/toolchains/linaro_toolchains_2014/arm-cortex_a9-linux-gnueabihf-linaro_4.9.3-2014.12"
export PATH=$__LINARO_TOOLCHAIN_PATH/bin:$PATH
export ARCH=arm
# export SUBARCH=arm
export CROSS_COMPILE=$__LINARO_TOOLCHAIN_PATH/bin/arm-eabi-
# export CROSS_COMPILE=$__LINARO_TOOLCHAIN_PATH/bin/
export INSTALL_MOD_PATH=./modules
export INSTALL_PATH=./install
