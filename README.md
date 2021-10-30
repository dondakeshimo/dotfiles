# dotfiles


# Install

### 1. Install requirements and setting zsh

##### If you use M1 Mac
I don't know why but one liner dosen't work.
I will search the reason, but temporally, I suggest download a code and run it.

```
$ curl -L -O raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/entrypoint/mac_full.sh
$ bash mac_full.sh
```

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
$ cd ~/src/github.com/dondakeshimo/dotfiles/setup/deployer
$ ./symlink.sh all
```

### (3. More)

- Use zsh
    - `chsh -s $(which zsh)`
    - if you use Mac
        - echo "<your zsh path>" >> /etc/shells
- Install teminal color scheme
    - `setup/installer/solarized/`
- Setup GitHub SSH connection
    - `ssh-keygen -t rsa`
    - filename: /absolute/path/to/your/home/.ssh/id\_git\_rsa
- Install nerd-fonts
    - https://github.com/ryanoasis/nerd-fonts
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
