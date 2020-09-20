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
            '-y' )
                FLAG_YES=true
                ;;
        esac
        shift
    done
}


confirm() {
    if "$FLAG_YES"; then
        return 0
    fi

    text=${1}

    echo -n "$text"
    read input

    if [ -z $input ] ; then
        echo "Please input yes or no."
        confirm_execution
    elif [ $input = 'yes' ] || [ $input = 'YES' ] || [ $input = 'y' ] ; then
        return 0
    elif [ $input = 'no' ] || [ $input = 'NO' ] || [ $input = 'n' ] ; then
        return 1
    else
        echo "Please input yes or no."
        confirm_execution
    fi
}


link_file() {
    local entry=$1
    local parent=${2:-$HOME}
    local filename=${entry##*/}
    local target=$parent/$filename
    local text="$target is already exist. Are you sure to overwrite? ( yes | no ): "

    echo "1 $entry $filename $parent"
    if [ -d $entry ]; then
        if [ ! -d $target ]; then mkdir $target; fi
        echo "2 $entry $filename $parent"
        for f in $entry/*; do
            link_file $f $target
        done
    elif [ -f $target ]; then
        if confirm "$text" ; then
            echo "3 $entry $filename $parent"
            ln -sf $PWD/$entry $parent
            echo "$entry is overwrittened."
        else
            echo "4 $entry $filename $parent"
            echo "$entry is skipped."
        fi
    else
        echo "5 $entry $filename $parent"
        ln -sf $PWD/$entry $parent
        echo "$entry is linked."
    fi
}


: "Link dotfiles" && {
    echo "${FLAG_EXEC[@]}"
    for f in "${FLAG_EXEC[@]}"
    do
        link_file $f $HOME
    done
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
