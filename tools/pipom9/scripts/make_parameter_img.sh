#!/usr/bin/bash

wget http://dl.radxa.com/rock/images/parameter/parameter_linux_sd
rkcrc -p parameter_linux_sd parameter.img  # where to get rkcrc, refer to http://radxa.com/Rock/flash_the_image "Flash with rkflashtool"

