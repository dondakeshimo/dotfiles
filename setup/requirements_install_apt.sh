#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

# confirm apt command exists
if ! has "apt"; then
    echo "apt is required"
    exit 1
fi


# install requirements via homebrew
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git \
    vim zsh tmux reattach-to-user-namespace golang fzy


# ghq setup
if ! has "go"; then
    echo "golang is something wrong"
    exit 1
fi
mkdir "$HOME/Scripts"
export GOPATH="$HOME/Scripts"
export PATH="$GOHOME/Scripts/bin:$PATH"
go get github.com/motemen/ghq
echo '[ghq]\n\troot = $HOME/Scripts/src' >> $HOME/.gitconfig


# install zplug
if ! has "zsh"; then
    echo "zsh is something wrong"
    exit 1
fi
curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh


# download my dotfiles
if ! has "ghq"; then
    echo "ghq is something wrong"
    exit 1
fi
ghq get https://github.com/dondakeshimo/dotfiles.git


# success message
echo
echo "Requirements installing is success!!"


