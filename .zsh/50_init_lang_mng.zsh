##############################
# PATH and environment settings
##############################

gcloud_components="/opt/homebrew/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/path.zsh.inc"
if [ -f $gcloud_components ]; then
    source $gcloud_components
fi

# go setting
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"
export ASDF_GOLANG_MOD_VERSION_ENABLED=true

# rust setting
export PATH="$HOME/.cargo/bin:$PATH"

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# direnv setting
if has "direnv"; then
    eval "$(direnv hook zsh)"
fi

# poetry setting
export PATH="$HOME/.poetry/bin:$PATH"
export POETRY_VIRTUALENVS_IN_PROJECT=true

# flutter with asdf setting
export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"
export PATH="$(asdf where flutter)/bin":"$PATH"
