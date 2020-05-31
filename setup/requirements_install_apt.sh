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
    sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python-openssl \
        git vim zsh tmux fzy

    # install golang from ppa:longsleep because of version
    sudo add-apt-repository -y ppa:longsleep/golang-backports
    sudo apt update
    sudo apt install golang-go
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
    go get -v github.com/motemen/ghq
    echo -e "[ghq]\n\troot = $HOME/Scripts/src" >> $HOME/.gitconfig
}


: "Use zsh" && {
    chsh -s $(which zsh)
}


: "Install zplug" && {
    if ! has "zsh"; then
        echo "zsh is something wrong"
        exit 1
    fi
    curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh
}


: "Echo success messages" && {
    echo
    echo "Requirements installing is success!!"
    echo "Please restart or logout to change shell to zsh"
    echo "And make symlink dotfiles by executing dotfiles/setup/symlink.sh"
    echo
    echo "If you want to use decorated NerdTree in vim, you have to install nerd-font"
    echo "https://github.com/ryanoasis/nerd-fonts"
}
