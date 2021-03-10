#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check os" && {
    if [[ "$(uname)" != "Darwin" ]]; then
        echo "This computer is not Mac"
        exit 1
    fi
}


: "Install homebrew" && {
    if has "brew"; then
        echo "Homebrew is already exist"
    else
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    fi
}


: "Install requirements" && {
    if ! has "brew"; then
        echo "Homebrew is something wrong"
        exit 1
    fi
    brew install git vim zsh tmux reattach-to-user-namespace fzy
}


: "Clone dotfiles repository" && {
    git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/deployer/symlink.sh"
}
