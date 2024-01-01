#!/usr/bin/bash

sudo apt-get install python-gtk2

HERE=$(dirname $(realpath ${BASH_SOURCE[0]}))
git clone https://github.com/RKLins/rkflashkit.git $HERE/../rkflashkit ;
cd ../rkflashkit
./waf debian
sudo dpkg -i rkflashkit_0.1.5_all.deb
