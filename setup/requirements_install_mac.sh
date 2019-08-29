#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

# confirm here is osx
if [[ "$(uname)" != "Darwin" ]]; then
    echo "This computer is not Mac"
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
brew install git vim zsh tmux reattach-to-user-namespace go


# ghq setup
mkdir "$HOME/Scripts"
export GOPATH="$HOME/Scripts"
echo '[ghq]\n\troot = $HOME/Scripts/src' >> $HOME/.gitconfig
go get github.com/motemen/ghq


# install zplug
curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh


# download my dotfiles
ghq get https://github.com/dondakeshimo/dotfiles.git


# success message
echo
echo "Requirements installing is success!!"

