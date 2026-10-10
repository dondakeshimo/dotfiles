#!/bin/bash

set -e

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
    sudo apt-get install -y git vim zsh tmux make build-essential wget curl neovim python3-neovim
}


: "Install sheldon" && {
    if ! has "sheldon"; then
        curl --proto '=https' -fLsS https://rossmacarthur.github.io/install/crate.sh \
            | bash -s -- --repo rossmacarthur/sheldon --to "$HOME/.local/bin"
    fi
}


: "Clone dotfiles repository" && {
    git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/deployer/symlink.sh"
}
