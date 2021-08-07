##############################
# zstyle
##############################

# completion conditions
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
zstyle ':completion:*' use-cache true
zstyle ':completion:*' verbose yes
zstyle ':completion:*:default' menu select=2
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'
zstyle ':completion:*:options' description 'yes'

# user zsh-completions directory
ZSH_USER_COMPLETIONS=$HOME/.zsh/zsh-completions
if [ ! -d "$ZSH_USER_COMPLETIONS" ]; then
    mkdir -p $ZSH_USER_COMPLETIONS
fi

# completion
if has "todo"; then
    # todo completion zsh > "$ZSH_USER_COMPLETIONS/_todo"
fi
