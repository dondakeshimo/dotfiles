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
    git clone https://github.com/aruhier/gnome-terminal-colors-solarized.git ~/src/github.com/aruhier/gnome-terminal-colors-solarized

    cd ~/src/github.com/aruhier/gnome-terminal-colors-solarized
    ./install.sh
}
