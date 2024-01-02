#!/bin/bash

HERE=$(dirname $(realpath ${BASH_SOURCE[0]}))
cd $HERE/..

# Prepare env
echo Setting up environment...
.  environment_linaro_2014.sh
echo ARCH=$ARCH
export MAKEFLAGS='--jobs=20 '$MAKEFLAGS
cd ../..

# Make
echo Invoking build...
make zImage

# Copy
cp $HERE/../../../arch/arm/boot/zImage $HERE/../zImage
echo zImage -- done
