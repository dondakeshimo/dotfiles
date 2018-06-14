#!/bin/bash

apm list --installed --bare > packages.txt

[ -f Brewfile ] && rm Brewfile
brew bundle dump
