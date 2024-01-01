#!/bin/bash

HERE=$(dirname $(realpath ${BASH_SOURCE[0]}))
echo Setting up environment...
cd $HERE/..
.  environment_linaro_2014.sh
echo ARCH=$ARCH
export MAKEFLAGS='--jobs=20 '$MAKEFLAGS
cd ../..

echo Building modules...
make INSTALL_MOD_PATH=$(pwd)/modules modules
make INSTALL_MOD_PATH=$(pwd)/modules modules_install
