##############################
# PATH and environment settings
##############################

# asdf setting
if [ -f $HOME/.asdf/asdf.sh ]; then
    . $HOME/.asdf/asdf.sh
    fpath=(${ASDF_DIR}/completions $fpath)
fi

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# direnv setting
if has "direnv"; then
    eval "$(direnv hook zsh)"
fi

# poetry setting
export PATH="$HOME/.poetry/bin:$PATH"
export POETRY_VIRTUALENVS_IN_PROJECT=true
