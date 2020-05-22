export CLICOLOR=true
export LSCOLORS='exfxcxdxbxGxDxabagacad'
export LS_COLORS='di=34:ln=35:so=32:pi=33:ex=31:bd=36;01:cd=33;01:su=31;40;07:sg=36;40;07:tw=32;40;07:ow=33;40;07:'
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='bg=black'
export EDITOR=vim
export HISTFILE=~/.zsh_history
export HISTSIZE=1000000
export SAVEHIST=1000000
export LANG=en_US.UTF-8

# PATH setting
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

# brew PATH setting
export PATH="/usr/local/bin:/usr/local/sbin:$PATH"

# go setting
export GOPATH="$HOME/Scripts"
export PATH="$GOPATH/bin:$PATH"

# poetry setting
export PATH="$HOME/.poetry/bin:$PATH"

# exclude waiting time
KEYTIMEOUT=1
