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
if has "nodebrew"; then
    export PATH="$HOME/.nodebrew/current/bin:$PATH"
fi

# gcc PATH setting for lightGBM
# export PATH="/usr/local/Cellar/gcc/8.1.0/bin:$PATH"

# Tex setting
if has "tex"; then
    export PATH="/Library/TeX/texbin:$PATH"
fi

# rbenv setting
if has "rbenv"; then
    export RBENV_ROOT="$HOME/.rbenv"
    export PATH="$RBENV_ROOT/bin:$PATH"
    export PATH="$RBENV_ROOT/shims:$PATH"
    eval "$(rbenv init -)"
fi

# direnv setting
if has "direnv"; then
    eval "$(direnv hook zsh)"
fi

# use mysql 5.6 first
export PATH="/usr/local/opt/mysql@5.6/bin:$PATH"

# gcloud setting
if has "gcloud"; then
    source "/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/path.zsh.inc"
    source "/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/completion.zsh.inc"
fi
