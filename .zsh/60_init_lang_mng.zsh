##############################
# PATH and environment settings
##############################

# pyenv setting
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# nodebrew setting
export PATH="$HOME/.nodebrew/current/bin:$PATH"

# gcc PATH setting for lightGBM
# export PATH="/usr/local/Cellar/gcc/8.1.0/bin:$PATH"

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# rbenv setting
export RBENV_ROOT="$HOME/.rbenv"
export PATH="$RBENV_ROOT/bin:$PATH"
export PATH="$RBENV_ROOT/shims:$PATH"
eval "$(rbenv init -)"

# direnv setting
eval "$(direnv hook zsh)"

# use mysql 5.6 first
export PATH="/usr/local/opt/mysql@5.6/bin:$PATH"
