source $HOME/.zsh/00_zshenv.zsh

# ------------------------ #
# zsh setting only on TMUX #
# ------------------------ #
if [ -z "$TMUX" ]; then
    $HOME/Scripts/bin/tmux-builder
else
    # ------------- #
    # setting zplug #
    # ------------- #
    export ZPLUG_HOME=$HOME/.zplug
    source $ZPLUG_HOME/init.zsh

    zplug 'zsh-users/zsh-autosuggestions'
    zplug 'zsh-users/zsh-completions'
    zplug 'zsh-users/zsh-syntax-highlighting', defer:2
    zplug "zsh-users/zsh-history-substring-search"
    zplug 'mollifier/anyframe'
    zplug "b4b4r07/enhancd", use:init.sh

    if ! zplug check --verbose; then
      printf 'Install? [y/N]: '
      if read -q; then
        echo; zplug install
      fi
    fi

    zplug load


    # ----------------------- #
    # setting zsh-completions #
    # ----------------------- #
    fpath=( \
        /usr/local/share/zsh-completions(N-/) \
        /usr/local/share/zsh/site-functions(N-/) \
        /usr/local/share/zsh/functions(N-/) \
        $fpath \
        )
    autoload -Uz compinit && compinit -u

    # ------------------------ #
    # load zsh utility modules #
    # ------------------------ #
    autoload -Uz add-zsh-hook
    autoload -Uz vcs_info
    autoload -Uz colors


    # ----------------------- #
    # load each setting files #
    # ----------------------- #
    for f in $HOME/.zsh/[0-9]*.(sh|zsh)
    do
        source "$f"
    done
fi
