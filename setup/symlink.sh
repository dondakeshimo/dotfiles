#!/bin/bash

cd `dirname $0`/../


function confirm_execution() {
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


for f in .??*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue
    [[ "$f" == ".zsh" ]] && continue

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


for f in bin/*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

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

