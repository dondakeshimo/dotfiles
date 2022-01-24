##############################
# PATH and environment settings
##############################

# asdf setting
if [ -f $ZPLUG_REPOS/asdf-vm/asdf/asdf.sh ]; then
    source $ZPLUG_REPOS/asdf-vm/asdf/asdf.sh
    fpath=(${ASDF_DIR}/completions(N-/) $fpath)
fi

# go setting
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# direnv setting
if has "direnv"; then
    eval "$(direnv hook zsh)"
fi

# poetry setting
export PATH="$HOME/.poetry/bin:$PATH"
export POETRY_VIRTUALENVS_IN_PROJECT=true
