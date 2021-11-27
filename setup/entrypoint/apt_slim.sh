#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check apt-get" && {
    if ! has "apt-get"; then
        echo "apt-get is required" 1>&2
        exit 1
    fi
}


: "Install requirementes" && {
    sudo apt-get update
    sudo apt-get install -y git vim wget make
}


: "Clone dotfiles repository" && {
    git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/deployer/symlink.sh"
}
