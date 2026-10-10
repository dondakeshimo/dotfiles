source $HOME/.zsh/00_zshenv.zsh

# ------------------------ #
# zsh setting only on TMUX #
# ------------------------ #
if [ -z "$TMUX" ]; then
    $HOME/bin/tmux-builder
    exit 0
fi

source $HOME/.zsh/sheldon.zsh

# ------------------------ #
# load zsh utility modules #
# ------------------------ #
autoload -Uz add-zsh-hook
autoload -Uz vcs_info
# `colors` populates $fg/$bg/$reset_color used by the prompt (70_prompt.zsh).
autoload -Uz colors && colors


# ----------------------- #
# load each setting files #
# ----------------------- #
for f in $HOME/.zsh/[0-9]*.(sh|zsh)
do
    source "$f"
done


# ----------------------- #
# setting zsh-completions #
# ----------------------- #
fpath=( \
    /usr/local/share/zsh-completions(N-/) \
    /usr/local/share/zsh/site-functions(N-/) \
    /usr/local/share/zsh/functions(N-/) \
    $HOME/.zsh/zsh-completions(N-/) \
    $fpath \
    )
autoload -Uz compinit && compinit -u


# ------------------------------------------- #
# os_detect set OS type to $PLATFORM variable #
# defined in 10_utils.zsh                     #
# ------------------------------------------- #
os_detect
