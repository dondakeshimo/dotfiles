# dotfiles


# Install

### 1. Install requirements and setting zsh

##### If you use Mac
```
$ bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/requirements_install_mac.sh)"
```

##### If you use Linux(apt)
```
$ bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/requirements_install_apt.sh)"
```

### 2. Deploy dotfiles
```
$ export GOPATH="$HOME/Scripts"
$ cd $GOPATH/src/github.com/dondakeshimo/dotfiles/setup
$ ./symlink.sh all
```


### 3. Restart or Logout


### (4. More)

- Install teminal color scheme
    - `setup/installer/solarized/`
- Install nerd-font
    - `setup/installer/install_nerdfont.sh`
    - `brew tap homebrew/cask-fonts; brew cask install <SOME NERD FONT>`
- Install Docker
    - https://docs.docker.com/engine/install/
- Install nvidia-docker
    - https://qiita.com/ksasaki/items/b20a785e1a0f610efa08
- Install pyenv


# Agreement
This repository's dotfiles are assume that bellow definitions.

```
BINARY PATH = ~/Scripts/bin
REPOSITORY PATH = ~/Scripts/src
REPOSITORY DIR RULE: equal to Golang
```

When you want to change these paths, BE CAREFUL with all of dotfiles.
