#!/bin/bash

HERE=$(realpath ${BASH_SOURCE[0]})
HERE=$(dirname ${HERE})

git clone https://github.com/RKLins/linaro.git ${HERE}/../linaro_toolchain
