#!/usr/bin/bash

if [ -z $RKDEVELOPTOOL ] ; then
	echo Error: RKDEVELOPTOOL env. variable must be set

	exit 1
fi

HERE=$(dirname $(realpath ${BASH_SOURCE[0]}))
cd $HERE/..

# Select image
ZIMAGE=$(find . -name 'str90-zimage*' | fzf)

# Flash image
sudo $RKDEVELOPTOOL wl 0xa000 $ZIMAGE
