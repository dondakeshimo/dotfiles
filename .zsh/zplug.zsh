##############################
# Set zplug
##############################

export ZPLUG_HOME=$HOME/.zplug

if [[ ! -f "$ZPLUG_HOME/init.zsh" ]]; then
    # install zplug
    curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh
fi

source $ZPLUG_HOME/init.zsh

zplug 'zplug/zplug', hook-build:'zplug --self-manage'
zplug 'zsh-users/zsh-autosuggestions'
zplug 'zsh-users/zsh-completions'
zplug 'zsh-users/zsh-syntax-highlighting', defer:2
zplug "zsh-users/zsh-history-substring-search"
zplug 'mollifier/anyframe'
zplug 'asdf-vm/asdf'
zplug "b4b4r07/enhancd", use:init.sh

if ! zplug check --verbose; then
  printf 'Install? [y/N]: '
  if read -q; then
    echo; zplug install
  fi
fi

zplug load
