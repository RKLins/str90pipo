#!/bin/bash

echo Setting up environment...
.  environment_linaro_2014.sh
echo ARCH=$ARCH
export MAKEFLAGS='--jobs=20 '$MAKEFLAGS
cd ../..

echo Configuring build...
make configure Pipo_M9Max_defconfig

echo Running menuconfig to generate .config file
make menuconfig
