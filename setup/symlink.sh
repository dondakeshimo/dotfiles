#!/bin/bash

cd `dirname $0`/../


FLAG_ZSH=false
FLAG_VIM=false
FLAG_TMUX=false
FLAG_GIT=false
FLAG_ATOM=false
FLAG_BIN=false
FLAG_SSH=false
FLAG_YES=false


function confirm_execution() {
    if "$FLAG_YES"; then
        return 0
    fi

    echo -n "$f already exists in $HOME. Do you overwrite it? (yes | no): "
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


for OPT in "$@"
do
    case $OPT in
        'all' )
            FLAG_ZSH=true
            FLAG_VIM=true
            FLAG_TMUX=true
            FLAG_GIT=true
            FLAG_ATOM=true
            FLAG_BIN=true
            ;;
        'dotfiles' )
            FLAG_ZSH=true
            FLAG_VIM=true
            FLAG_TMUX=true
            FLAG_GIT=true
            FLAG_SSH=true
            ;;
        'zsh' )
            FLAG_ZSH=true
            ;;
        'vim' )
            FLAG_VIM=true
            ;;
        'tmux' )
            FLAG_TMUX=true
            ;;
        'git' )
            FLAG_GIT=true
            ;;
        'ssh' )
            FLAG_SSH=true
            ;;
        'atom' )
            FLAG_ATOM=true
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


: "Link dotfiles" && {
    for f in .??*
    do
        # ignore below files or directories
        [[ "$f" == ".git" ]] && continue
        [[ "$f" == ".DS_Store" ]] && continue
        [[ "$f" == ".zsh" ]] && continue
        [[ "$f" == ".ssh" ]] && continue
        [[ "$f" == ".jupyter" ]] && continue

        # check flag
        [[ "$f" == ".zshrc" ]] && if ! "$FLAG_ZSH"; then continue; fi
        [[ "$f" == ".vimrc" ]] && if ! "$FLAG_VIM"; then continue; fi
        [[ "$f" == ".tmux.conf" ]] && if ! "$FLAG_TMUX"; then continue; fi
        [[ "$f" == ".gitconfig" ]] && if ! "$FLAG_GIT"; then continue; fi

        if [ -e $HOME/$f ]; then
            if confirm_execution; then
                ln -sf $PWD/$f $HOME
                echo "$f is overwrittened."
            else
                echo "$f is skipped."
                continue
            fi
        else
            echo "$f is linked."
            ln -sf $PWD/$f $HOME
        fi
    done
}


: "Link .ssh" && {
    if "$FLAG_SSH"; then
        f=.ssh/config
        if [ -e $HOME/$f ]; then
            if confirm_execution; then
                ln -sf $PWD/$f $HOME/.ssh
                echo "$f is overwrittened."
            else
                echo "$f is skipped."
            fi
        else
            if [ ! -d $HOME/.ssh ]; then
                mkdir $HOME/.ssh
            fi

            ln -sf $PWD/$f $HOME/.ssh
            echo "$f is linked."
        fi
    fi
}


: "Link zsh/" && {
    if "$FLAG_ZSH"; then
        for f in .zsh/*
        do
            [[ "$f" == ".git" ]] && continue
            [[ "$f" == ".DS_Store" ]] && continue

            if [ -e $HOME/$f ]; then
                if confirm_execution; then
                    ln -sf $PWD/$f $HOME/.zsh
                    echo "$f is overwrittened."
                else
                    echo "$f is skipped."
                    continue
                fi
            else
                if [ ! -d $HOME/.zsh ]; then
                    mkdir $HOME/.zsh
                fi

                ln -sf $PWD/$f $HOME/.zsh
                echo "$f is linked."
            fi
        done
    fi
}


: "Link Atom config" && {
    if "$FLAG_ATOM"; then
        for f in atom/*
        do
            [[ "$f" == ".git" ]] && continue
            [[ "$f" == ".DS_Store" ]] && continue

            if [ -e $HOME/$f ]; then
                if confirm_execution; then
                    ln -sf $PWD/$f $HOME/.atom
                    echo "$f is overwrittened."
                else
                    echo "$f is skipped."
                    continue
                fi
            else
                if [ ! -d $HOME/.atom ]; then
                    echo "atom is not installed"
                    break
                fi

                echo "$f is linked."
                ln -sf $PWD/$f $HOME/.atom
            fi
        done
    fi
}


: "Link common binary" && {
    if "$FLAG_BIN"; then
        for f in bin/*
        do
            [[ "$f" == ".git" ]] && continue
            [[ "$f" == ".DS_Store" ]] && continue
            [ -d "$f" ] && continue

            if [ -e $GOPATH/$f ]; then
                if confirm_execution; then
                    ln -sf $PWD/$f $GOPATH/bin
                    echo "$f is overwrittened."
                else
                    echo "$f is skipped."
                    continue
                fi
            else
                if [ ! -d $GOPATH/bin ]; then
                    mkdir $GOPATH/bin
                fi

                ln -sf $PWD/$f $GOPATH/bin
                echo "$f is linked."
            fi
        done
    fi
}


: "Link os specific binary" && {
    if ! "$FLAG_BIN"; then exit 0;fi
    if "$FLAG_BIN" && [ $(uname) = 'Linux' ]; then ostype="linux"; fi
    if "$FLAG_BIN" && [ $(uname) = 'Darwin' ]; then ostype="osx"; fi

    for f in bin/"$ostype"/*
    do
        file=${f##*/}
        [[ "$file" == ".git" ]] && continue
        [[ "$file" == ".DS_Store" ]] && continue

        if [ -e "$GOPATH/bin/$file" ]; then
            echo "$GOPATH/bin/$file"
            if confirm_execution; then
                ln -sf $PWD/$f $GOPATH/bin
                echo "$f is overwrittened."
            else
                echo "$f is skipped."
                continue
            fi
        else
            echo "$GOPATH/bin/$file"
            if [ ! -d $GOPATH/bin ]; then
                mkdir $GOPATH/bin
            fi

            ln -sf $PWD/$f $GOPATH/bin
            echo "$f is linked."
        fi
    done
}
