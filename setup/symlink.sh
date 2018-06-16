#!/bin/bash

cd `dirname $0`/../

for f in .??*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

    ln -sf $PWD/$f $HOME
    echo "$f"
done

for f in atom/*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

    ln -sf $PWD/$f $HOME/.atom
    echo "$f"
done

for f in bin/*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

    ln -sf $PWD/$f $HOME/Scripts/bin
    echo "$f"
done
