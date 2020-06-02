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
    yum install -y gcc zlib-devel bzip2 bzip2-devel readline-devel\
                   sqlite sqlite-devel openssl-devel tk-devel libffi-devel\
                   git vim zsh fzy

    sudo yum install -y epel-release
    sudo yum install -y golang
}


: "Install ghq" && {
    # check go exist
    if ! has "go"; then
        echo "golang is something wrong"
        exit 1
    fi

    # go setting
    mkdir "$HOME/Scripts"
    export GOPATH="$HOME/Scripts"
    export PATH="$GOPATH/bin:$PATH"

    # install ghq
    go get -v github.com/x-motemen/ghq
    echo -e "[ghq]\n\troot = $HOME/Scripts/src" >> $HOME/.gitconfig
}


: "Use zsh" && {
    chsh -s $(which zsh)
}


: "Clone dotfiles repository" && {
    ghq get https://github.com/dondakeshimo/dotfiles.git
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please make symlink dotfiles by executing dotfiles/setup/symlink.sh"
    echo
    echo "If you want to use decorated NerdTree in vim, you have to install nerd-font"
    echo "https://github.com/ryanoasis/nerd-fonts"
}
