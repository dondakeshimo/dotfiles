#!/bin/bash

cd `dirname $0`/../../


: "Define global variables" && {
    FLAG_EXEC=()
    FLAG_BIN=false
    BIN_DIR=~/bin
    ZSH_TGT=(".zshrc" ".zsh")
    BASH_TGT=(".bash_profile" ".bash_prompt")
    VIM_TGT=(".vimrc")
    CFG_TGT=(".config")
    TMUX_TGT=(".tmux.conf")
    GIT_TGT=(".gitconfig" ".gitignore_global")
    SSH_TGT=(".ssh")
    ATOM_TGT=(".atom")
    ASDF_TGT=(".asdfrc")
    DOTFILES_TGT=(${ZSH_TGT[@]} ${BASH_TGT[@]} ${VIM_TGT[@]} ${CFG_TGT[@]} ${TMUX_TGT[@]} ${GIT_TGT[@]} ${SSH_TGT[@]} ${ATOM_TGT[@]} ${ASDF_TGT[@]})
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
                FLAG_EXEC=(${FLAG_EXEC[@]} ${DOTFILES_TGT[@]})
                FLAG_BIN=true
                ;;
            'dotfiles' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${DOTFILES_TGT[@]})
                ;;
            'zsh' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${ZSH_TGT[@]})
                ;;
            'bash' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${BASH_TGT[@]})
                ;;
            'vim' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${VIM_TGT[@]})
                ;;
            'config' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${CFG_TGT[@]})
                ;;
            'tmux' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${TMUX_TGT[@]})
                ;;
            'git' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${GIT_TGT[@]})
                ;;
            'ssh' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${SSH_TGT[@]})
                ;;
            'atom' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${ATOM_TGT[@]})
                ;;
            'asdf' )
                FLAG_EXEC=(${FLAG_EXEC[@]} ${ASDF_TGT[@]})
                ;;
            'bin' )
                FLAG_BIN=true
                ;;
        esac
        shift
    done
}


# link_file is a domain rule.
link_file() {
    local entry=$1
    local parent=${2:-$HOME}
    local filename=${entry##*/}
    local target=$parent/$filename

    echo "entry: $entry, parent: $parent, filename: $filename, target: $target"
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
    echo "Target dotfiles: [ ${FLAG_EXEC[@]} ]"
    for f in "${FLAG_EXEC[@]}"
    do
        link_file $f $HOME
    done
}


: "Make directory .vimbackup" && {
    if $(echo ${FLAG_EXEC[@]} | grep -q "vim"); then
        if [ ! -d $HOME/.vimbackup ]; then mkdir $HOME/.vimbackup; fi
    fi
}


: "Link binary" && {
    if ! "$FLAG_BIN"; then exit 0;fi

    if "$FLAG_BIN" && [ $(uname) = 'Linux' ]; then ostype="linux"; fi
    if "$FLAG_BIN" && [ $(uname) = 'Darwin' ]; then ostype="osx"; fi

    if [ ! -d $BIN_DIR ]; then mkdir -p $BIN_DIR; fi

    for f in bin/*
    do
        [[ "$f" == ".git" ]] && continue
        [[ "$f" == ".DS_Store" ]] && continue
        [ -d "$f" ] && continue

        link_file $f $BIN_DIR
    done

    for f in bin/"$ostype"/*
    do
        [[ "$f" == ".git" ]] && continue
        [[ "$f" == ".DS_Store" ]] && continue

        link_file $f $BIN_DIR
    done
}
