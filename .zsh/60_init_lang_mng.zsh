##############################
# PATH and environment settings
##############################

# pyenv setting
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if has "pyenv"; then
    eval "$(pyenv init -)"
fi

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
if has "rbenv"; then
    eval "$(rbenv init -)"
fi

# direnv setting
if has "direnv"; then
    eval "$(direnv hook zsh)"
fi

# use mysql 5.6 first
# export PATH="/usr/local/opt/mysql@5.6/bin:$PATH"

# gcloud setting
# TODO: linux対応
if has "gcloud" && is_osx; then
    source "/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/path.zsh.inc"
    source "/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/completion.zsh.inc"
fi
