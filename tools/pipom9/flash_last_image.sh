#!/bin/bash

PYTHON="python3"

echo using python $PYTHON

# Find last image
LAST_IMAGE=$(ls -la | grep bin | awk '{print $9'} | sort | tail -n 1)
echo LAST_IMAGE=$LAST_IMAGE

if [ "$LAST_IMAGE" ==  "" ] ; then
	echo "Couldn't find the last image"
	exit 1
fi

# Flash
FLASHING_COMMAND="sudo python3 ./rkflashkit/run.py flash @boot $LAST_IMAGE"
echo Flashing image... $FLASHING_COMMAND
$FLASHING_COMMAND
