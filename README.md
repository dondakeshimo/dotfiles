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

### 2. Restart or Logout


### 3. Export GOPATH
```
$ export GOPATH="$HOME/Scripts"
```


### 4. Download this repository

```
$ ghq get https://github.com/dondakeshimo/dotfiles.git
```

### 5. Deploy dotfiles

```
$ cd $HOME/Scripts/src/github.com/dondakeshimo/dotfiles/setup
$ ./symlink.sh all
```

