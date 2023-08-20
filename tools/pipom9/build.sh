#!/bin/bash

echo Setting up environment...
.  environment_linaro_2014.sh
echo ARCH=$ARCH
export MAKEFLAGS='--jobs=4'
cd ../..

echo Invoking build...
make zImage
