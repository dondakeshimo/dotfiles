# dotfiles


# Install

### 1. Install requirements and setting zsh

##### If you use Mac
```
$ bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/entrypoint/mac_full.sh)"
```

##### If you use Linux(apt)
```
$ bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/entrypoint/apt_full.sh)"
```

### 2. Deploy dotfiles
```
$ cd ~/src/github.com/dondakeshimo/dotfiles/setup
$ ./symlink.sh all
```


### (4. More)

- Install teminal color scheme
    - `setup/installer/solarized/`
- Install Docker
    - [how to install](https://docs.docker.com/engine/install/)
- Install nvidia-docker
    - [how to install](https://medium.com/nvidiajapan/nvidia-docker-%E3%81%A3%E3%81%A6%E4%BB%8A%E3%81%A9%E3%81%86%E3%81%AA%E3%81%A3%E3%81%A6%E3%82%8B%E3%81%AE-20-09-%E7%89%88-558fae883f44)


# Agreement
This repository's dotfiles are assume that bellow definitions.

```
BINARY PATH = ~/bin
REPOSITORY PATH = ~/src
REPOSITORY PLACEMENT RULE: equal to Golang pkg
```

When you want to change these paths, BE CAREFUL with all of dotfiles.
