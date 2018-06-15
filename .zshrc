##############################
# zplug
##############################

export ZPLUG_HOME=/usr/local/opt/zplug
source $ZPLUG_HOME/init.zsh

zplug 'zsh-users/zsh-autosuggestions'
zplug 'zsh-users/zsh-completions'
zplug "themes/ys", from:oh-my-zsh
zplug 'zsh-users/zsh-syntax-highlighting', defer:2
zplug "zsh-users/zsh-history-substring-search", hook-build:"__zsh_version 5.4"
zplug 'mollifier/anyframe'
zplug "b4b4r07/enhancd", use:init.sh

if ! zplug check --verbose; then
  printf 'Install? [y/N]: '
  if read -q; then
    echo; zplug install
  fi
fi

zplug load


##############################
# Autoloadings
##############################

# zsh-completionsの設定
fpath=(/usr/local/share/zsh/site-functions(N-/) $fpath)
autoload -Uz compinit && compinit -u

# autoload -Uz add-zsh-hook
autoload -Uz vcs_info


##############################
# General settings
##############################

setopt auto_list
setopt auto_menu
setopt auto_pushd
setopt extended_history
setopt hist_ignore_all_dups
setopt hist_ignore_dups
setopt hist_reduce_blanks
setopt hist_save_no_dups
setopt ignore_eof
setopt inc_append_history
setopt interactive_comments
setopt no_beep
setopt no_hist_beep
setopt no_list_beep
setopt magic_equal_subst
setopt notify
setopt print_eight_bit
setopt print_exit_value
setopt prompt_subst
setopt pushd_ignore_dups
setopt rm_star_wait
setopt share_history
setopt transient_rprompt


##############################
# Key bindings
##############################

bindkey -v
bindkey -M viins '^?'  backward-delete-char
bindkey -M viins '^A'  beginning-of-line
bindkey -M viins '^B'  backward-char
bindkey -M viins '^D'  delete-char-or-list
bindkey -M viins '^E'  end-of-line
bindkey -M viins '^F'  forward-char
bindkey -M viins '^G'  send-break
bindkey -M viins '^H'  backward-delete-char
bindkey -M viins '^N'  history-substring-search-down
bindkey -M viins '^P'  history-substring-search-up
bindkey -M viins '^W'  backward-kill-word
bindkey -M viins '^@'  anyframe-widget-put-history


##############################
# Aliases
##############################

alias vi='vim'
alias ll='ls -l'
alias la='ls -a'
alias rm='rmtrash'
alias brew='env PATH=${PATH/\/Users\/${USER}\/\.pyenv\/shims:/} brew'


##############################
# zstyle
##############################

# Completion
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
zstyle ':completion:*' use-cache true
zstyle ':completion:*' verbose yes
zstyle ':completion:*:default' menu select=2
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'
zstyle ':completion:*:options' description 'yes'


##############################
# zsh env
##############################

export CLICOLOR=true
export LSCOLORS='exfxcxdxbxGxDxabagacad'
export LS_COLORS='di=34:ln=35:so=32:pi=33:ex=31:bd=36;01:cd=33;01:su=31;40;07:sg=36;40;07:tw=32;40;07:ow=33;40;07:'
export EDITOR=vim
export HISTFILE=~/.zsh_history
export HISTSIZE=1000000
export SAVEHIST=1000000
export LANG=ja_JP.UTF-8


##############################
# PATH and environment settings
##############################

# PATH setting
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

# brew PATH setting
export PATH="/usr/local/bin:/usr/local/sbin:$PATH"

# gcc PATH setting for lightGBM
export PATH="/usr/local/Cellar/gcc/8.1.0/bin:$PATH"

# pyenv setting
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# nodebrew setting
export PATH="$HOME/.nodebrew/current/bin:$PATH"

# go setting
export GOPATH="$HOME/Scripts"
export PATH="$GOPATH/bin:$PATH"

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# exclude waiting time
KEYTIMEOUT=1


##############################
# tmux
##############################

tmux-builder


##############################
# ZLE settings
##############################



##############################
# hash
##############################
