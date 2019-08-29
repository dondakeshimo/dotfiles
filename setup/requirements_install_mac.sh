#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

# confirm here is osx
if [[ "$(uname)" != "Darwin" ]]; then
    echo "This computer is not Mac"
    exit 1
fi


# install homebrew
if has "brew"; then
    echo "Homebrew is already exist"
else
    if has "/usr/bin/ruby"; then
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    else; then
        echo "Ruby is requred. OSX consists Ruby. Is this OSX allright?"
        exit 1
    fi
fi


# install requirements via homebrew
if ! has "brew"; then
    echo "Homebrew is something wrong"
    exit 1
fi
brew install git vim zsh tmux reattach-to-user-namespace go


# ghq setup
if ! has "go"; then
    echo "golang is something wrong"
    exit 1
fi
mkdir "$HOME/Scripts"
export GOPATH="$HOME/Scripts"
export PATH="$GOHOME/Scripts/bin:$PATH"
echo '[ghq]\n\troot = $HOME/Scripts/src' >> $HOME/.gitconfig
go get github.com/motemen/ghq


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

