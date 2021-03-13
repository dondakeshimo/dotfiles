#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check yum" && {
    if ! has "yum"; then
        echo "yum is required" 1>&2
        exit 1
    fi
}


: "Install requirementes" && {
    sudo yum update
    yum install -y git vim curl wget make
}


: "Clone dotfiles repository" && {
    git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/deployer/symlinksh"
}
