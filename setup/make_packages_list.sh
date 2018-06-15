#!/bin/bash

cd `dirname $0`/../

apm list --installed --bare > package_lists/packages.txt

[ -f Brewfile ] && rm Brewfile
brew bundle dump && mv Brewfile package_lists/Brewfile
