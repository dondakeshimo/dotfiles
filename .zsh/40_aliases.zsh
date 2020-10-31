##############################
# Aliases
##############################

# no use vi
alias v='nvim'
alias vi='nvim'
alias vim='nvim'

# ls aliases frequentry use
alias ll='ls -l'
alias la='ls -a'
alias lla='ls -la'

# overwrite rm with rmtrash which move to trash of os
(( $+commands[rmtrash] )) && alias rm='rmtrash'

# to use gcc version 7
#(( $+commands[gcc-7] )) && alias gcc='gcc-7'
#(( $+commands[g++-7] )) && alias g++='g++-7'

# short cut bundle exec for rails
(( $+commands[bundle] )) && alias be='bundle exec'

# short cut airport command
alias airport='/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'

# fzy util
alias treecd='tree --charset=o -f | fzy | tr -d '"'"'\||`|-'"'"' | xargs echo | cd'
alias gcd='ghq list --full-path | fzy | xargs echo | cd'
