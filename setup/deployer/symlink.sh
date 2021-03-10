#!/bin/bash


: "Define global variables" && {
    FLAG_EXEC=()
    FLAG_BIN=false
    BIN_DIR=~/bin
    ZSH_TGT=(".zshrc" ".zsh")
    BASH_TGT=(".bash_profile" ".bashprompt")
    VIM_TGT=(".vimrc" ".vim")
    TMUX_TGT=(".tmux.conf")
    GIT_TGT=(".gitconfig" ".gitignore_global")
    SSH_TGT=(".ssh")
    ATOM_TGT=(".atom")
    ASDF_TGT=(".asdfrc")
    DOTFILES_TGT=(${ZSH_TGT[@]} ${BASH_TGT[@]} ${VIM_TGT[@]} ${TMUX_TGT[@]} ${GIT_TGT[@]} ${SSH_TGT[@]} ${ATOM_TGT[@]} ${ASDF_TGT[@]})
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
                FLAG_EXEC=(${DOTFILES_TGT[@]})
                FLAG_BIN=true
                ;;
            'dotfiles' )
                FLAG_EXEC=(${DOTFILES_TGT[@]})
                ;;
            'zsh' )
                FLAG_EXEC=(${ZSH_TGT[@]})
                ;;
            'bash' )
                FLAG_EXEC=(${BASH_TGT[@]})
                ;;
            'vim' )
                FLAG_EXEC=(${VIM_TGT[@]})
                ;;
            'tmux' )
                FLAG_EXEC=(${TMUX_TGT[@]})
                ;;
            'git' )
                FLAG_EXEC=(${GIT_TGT[@]})
                ;;
            'ssh' )
                FLAG_EXEC=(${SSH_TGT[@]})
                ;;
            'atom' )
                FLAG_EXEC=(${ATOM_TGT[@]})
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
    local text="$target is already exist.\nAre you sure to overwrite? ( yes | no ): "

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


: "Link vimrc for nvim" && {
    if $(echo ${FLAG_EXEC[@]} | grep -q "vim"); then
        target="$HOME/.config/nvim"
        if [ ! -d $target ]; then mkdir -p $target; fi
        ln -svi $PWD/.vimrc $target/init.vim
        ln -svi $PWD/.vim/coc-settings.json $target
        ln -svi $PWD/.vim/ftplugin $target
        ln -svi $PWD/.vim/dein $target
    fi
}


: "Link binary" && {
    if ! "$FLAG_BIN"; then exit 0;fi

    if "$FLAG_BIN" && [ $(uname) = 'Linux' ]; then ostype="linux"; fi
    if "$FLAG_BIN" && [ $(uname) = 'Darwin' ]; then ostype="osx"; fi

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
