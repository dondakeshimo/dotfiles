#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check apt" && {
    if ! has "apt"; then
        echo "apt is required" 1>&2
        exit 1
    fi
}

: "Install requirementes" && {
    sudo apt update
    sudo apt install -y dconf-cli
}

: "Install gnome-terminal-colors-solarized" && {
    ghq get https://github.com/aruhier/gnome-terminal-colors-solarized.git
    cd $GOPATH/src/github.com/aruhier/gnome-terminal-colors-solarized
    ./install.sh
}
