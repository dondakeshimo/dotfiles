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
    sudo apt install -y git vim zsh tmux fzy make build-essential wget curl
}


: "Clone dotfiles repository" && {
    git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/deployer/symlink.sh"
}
