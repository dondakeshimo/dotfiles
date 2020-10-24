#!/bin/bash

cd `dirname $0`/../


: "Define global variables" && {
    FLAG_EXEC=()
    FLAG_BIN=false
    FLAG_YES=false
}


: "Check arguments" && {
    if [ $# == 0 ]; then
        echo "illegal arguments"
        exit 1
    fi
}


: "Parse arguments" && {
    for OPT in "$@"
    do
        case $OPT in
            'all' )
                FLAG_EXEC=(".zshrc" ".zsh" ".vimrc" ".vim" ".tmux.conf" ".gitconfig" ".atom" ".ssh")
                FLAG_BIN=true
                ;;
            'dotfiles' )
                FLAG_EXEC=(".zshrc" ".zsh" ".vimrc" ".vim" ".tmux.conf" ".gitconfig" ".atom" ".ssh")
                ;;
            'zsh' )
                FLAG_EXEC=(".zshrc" ".zsh")
                ;;
            'vim' )
                FLAG_EXEC=(".vimrc" ".vim")
                ;;
            'tmux' )
                FLAG_EXEC=(".tmux.conf")
                ;;
            'git' )
                FLAG_EXEC=(".gitconfig")
                ;;
            'ssh' )
                FLAG_EXEC=(".ssh")
                ;;
            'atom' )
                FLAG_EXEC=(".atom")
                ;;
            'bin' )
                FLAG_BIN=true
                ;;
        esac
        shift
    done
}


link_file() {
    local entry=$1
    local parent=${2:-$HOME}
    local filename=${entry##*/}
    local target=$parent/$filename
    local text="$target is already exist. Are you sure to overwrite? ( yes | no ): "

    if [ -d $entry ]; then
        if [ ! -d $target ]; then mkdir $target; fi
        for f in $entry/*; do
            link_file $f $target
        done
    elif [ -f $target ]; then
        ln -svi $PWD/$entry $parent
    else
        ln -svi $PWD/$entry $parent
    fi
}


: "Link dotfiles" && {
    echo "${FLAG_EXEC[@]}"
    for f in "${FLAG_EXEC[@]}"
    do
        link_file $f $HOME
    done
}


: "Link vimrc for nvim" && {
    if $(echo ${FLAG_EXEC[@]} | grep -q "vim"); then
        target="$HOME/.config/nvim"
        if [ ! -d $target ]; then mkdir -p $target; fi
        ln -svi $PWD/.vimrc $target/init.vim
        ln -svi $PWD/.vim/ftplugins $target
    fi
}


: "Link binary" && {
    if ! "$FLAG_BIN"; then exit 0;fi

    if "$FLAG_BIN" && [ $(uname) = 'Linux' ]; then ostype="linux"; fi
    if "$FLAG_BIN" && [ $(uname) = 'Darwin' ]; then ostype="osx"; fi

    if [ ! "{$GOPATH:+isdefined}" ]; then
        echo 'You must define $GOPATH'
        echo 'example:'
        echo '$ export GOPATH="$HOME/Scripts"'
        exit 1
    fi

    for f in bin/*
    do
        [[ "$f" == ".git" ]] && continue
        [[ "$f" == ".DS_Store" ]] && continue
        [ -d "$f" ] && continue

        link_file $f $GOPATH/bin
    done

    for f in bin/"$ostype"/*
    do
        [[ "$f" == ".git" ]] && continue
        [[ "$f" == ".DS_Store" ]] && continue

        link_file $f $GOPATH/bin
    done
}
