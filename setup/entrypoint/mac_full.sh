#!/bin/bash

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check osx" && {
    if [[ "$(uname)" != "Darwin" ]]; then
        echo "This computer is not Mac"
        exit 1
    fi
}


: "Install homebrew" && {
    if has "brew"; then
        echo "Homebrew is already exist"
    else
        if has "/usr/bin/ruby"; then
            /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        else
            echo "Ruby is required. OSX consists Ruby. Is this OSX allright?"
            exit 1
        fi
    fi
}


: "Install requirements" && {
    if ! has "brew"; then
        echo "Homebrew is something wrong"
        exit 1
    fi
    brew install git vim zsh tmux reattach-to-user-namespace go fzy
}


: "Install ghq" && {
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