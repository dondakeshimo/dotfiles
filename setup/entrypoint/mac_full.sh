#!/bin/bash

set -e

REPO=$HOME/src/github.com/dondakeshimo/dotfiles


: "Run mac_core" && {
    if [ -f "$REPO/setup/entrypoint/mac_core.sh" ]; then
        bash "$REPO/setup/entrypoint/mac_core.sh"
    else
        bash -c "$(curl -fsSL https://raw.githubusercontent.com/dondakeshimo/dotfiles/main/setup/entrypoint/mac_core.sh)"
    fi

    # mac_core runs in a child process, so re-apply Homebrew's environment.
    if [ -x /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
}


: "Install mise tools" && {
    mise install
}


: "Install rustup" && {
    if [ -x "$HOME/.cargo/bin/rustup" ]; then
        echo "rustup is already installed"
    else
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
    fi
    # cargo is only available after a toolchain is installed.
    export PATH="$HOME/.cargo/bin:$PATH"
    rustup default stable
}


: "Install alacritty" && {
    # The Homebrew cask is disabled (Gatekeeper), so build from source.
    # https://github.com/alacritty/alacritty/blob/master/INSTALL.md#macos
    if [ -d /Applications/Alacritty.app ]; then
        echo "Alacritty is already installed"
    else
        export PATH="$HOME/.cargo/bin:$PATH"
        ALACRITTY=$HOME/src/github.com/alacritty/alacritty
        if [ -d "$ALACRITTY" ]; then
            echo "Alacritty source is already cloned"
        else
            git clone https://github.com/alacritty/alacritty.git "$ALACRITTY"
        fi
        (cd "$ALACRITTY" && rustup override set stable && rustup update stable && make app)
        cp -r "$ALACRITTY/target/release/osx/Alacritty.app" /Applications/
        tic -xe alacritty,alacritty-direct -o "$HOME/.terminfo" "$ALACRITTY/extra/alacritty.info" 2>/dev/null || true
    fi
}


: "Install alacritty theme" && {
    # Alacritty's config imports ~/.config/alacritty/themes/themes/solarized_dark.toml.
    # https://github.com/alacritty/alacritty-theme#imports
    ALACRITTY_THEME=$HOME/.config/alacritty/themes
    if [ -d "$ALACRITTY_THEME" ]; then
        echo "Alacritty theme is already cloned"
    else
        mkdir -p "$(dirname "$ALACRITTY_THEME")"
        git clone https://github.com/alacritty/alacritty-theme.git "$ALACRITTY_THEME"
    fi
}


: "Configure 1Password SSH agent" && {
    # Expose the agent at a stable path shared with Linux (~/.1password/agent.sock).
    ONEPASSWORD_SOCKET="$HOME/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
    if [ -d /Applications/1Password.app ]; then
        mkdir -p "$HOME/.1password"
        ln -sf "$ONEPASSWORD_SOCKET" "$HOME/.1password/agent.sock"
        if [ ! -S "$ONEPASSWORD_SOCKET" ]; then
            echo
            echo "NOTE: The 1Password SSH Agent isn't running yet."
            echo "      1. Open 1Password and sign in."
            echo "      2. Settings > Developer > turn on \"Use the SSH Agent\"."
            echo "      3. Settings > General > keep 1Password running (menu bar / start at login)."
            echo "      ~/.1password/agent.sock will start working automatically once enabled."
            echo
        fi
    fi
}


: "Echo success messages" && {
    echo
    echo "Setup is success!!"
}
