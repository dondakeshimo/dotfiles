# dotfiles

## Agreement

This repository's dotfiles are assume that bellow definitions.

```bash
BINARY PATH = ~/bin
REPOSITORY PATH = ~/src
REPOSITORY PLACEMENT RULE: equal to Golang pkg
```

When you want to change these paths, BE CAREFUL with all of dotfiles.

## Setup

### 1. Setup requirements

#### macOS

The macOS script installs Homebrew, applies `setup/entrypoint/Brewfile`, clones this repository, deploys the dotfiles (symlink), installs mise tools, installs rustup, builds Alacritty from source, and clones the Alacritty theme. It runs `mac_core.sh` (Homebrew, Brewfile, clone, symlink) first and then adds mise, rustup, Alacritty and its theme; CI uses `mac_core.sh` directly.

```bash
$ bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/main/setup/entrypoint/mac_full.sh)"
```

#### Linux (Out of maintenance)

Now, there are no maintained linux entrypoints because I don't use any Linux machines for my development.

### 2. Deploy dotfiles

`mac_full.sh` already deploys them, but you can re-run the deployer any time.

```bash
$ cd ~/src/github.com/dondakeshimo/dotfiles/setup/deployer
$ ./symlink.sh all
```
