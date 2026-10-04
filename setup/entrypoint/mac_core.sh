#!/bin/bash

set -e

has() {
    type "${1:?too few arguments}" &>/dev/null
}

: "Check os" && {
    if [[ "$(uname)" != "Darwin" ]]; then
        echo "This computer is not Mac"
        exit 1
    fi
}


: "Install homebrew" && {
    if has "brew"; then
        echo "Homebrew is already exist"
    else
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Make brew available in this non-interactive shell (Apple Silicon).
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    if ! has "brew"; then
        echo "Homebrew is something wrong"
        exit 1
    fi
}


: "Clone dotfiles repository" && {
    REPO=$HOME/src/github.com/dondakeshimo/dotfiles
    if [ -d "$REPO" ]; then
        echo "Repository is already cloned"
    else
        git clone https://github.com/dondakeshimo/dotfiles.git "$REPO"
    fi
}


: "Install bundles" && {
    # GUI casks can't be installed in CI.
    if [ -n "$CI" ]; then
        export HOMEBREW_BUNDLE_CASK_SKIP=1
    fi
    brew bundle install --file="$REPO/setup/entrypoint/Brewfile" --no-upgrade
}


: "Deploy dotfiles" && {
    "$REPO/setup/deployer/symlink.sh" all
}
