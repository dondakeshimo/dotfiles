#!/bin/bash

FONT=$1

git clone --branch=master --depth 1 https://github.com/ryanoasis/nerd-fonts.git
cd nerd-fonts
./install.sh ${FONT}
cd ..
rm -rf nerd-fonts
