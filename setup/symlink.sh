#!/bin/bash

cd `dirname $0`/../

for f in .??*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

    ln -sf $PWD/$f ~/$f
    echo "$f"
done

for f in atom/*
do
    [[ "$f" == ".git" ]] && continue
    [[ "$f" == ".DS_Store" ]] && continue

    ln -sf $PWD/$f ~/.$f
    echo "$f"
done
