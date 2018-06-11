##############################
# zplug
##############################

export ZPLUG_HOME=/usr/local/opt/zplug
source $ZPLUG_HOME/init.zsh

zplug 'zsh-users/zsh-autosuggestions'
zplug 'zsh-users/zsh-completions'
zplug "themes/ys", from:oh-my-zsh
zplug 'zsh-users/zsh-syntax-highlighting', defer:2
zplug "zsh-users/zsh-history-substring-search", hook-build:"__zsh_version 5.4"
zplug 'mollifier/anyframe'
zplug "b4b4r07/enhancd", use:init.sh

if ! zplug check --verbose; then
  printf 'Install? [y/N]: '
  if read -q; then
    echo; zplug install
  fi
fi

zplug load


##############################
# Autoloadings
##############################

# zsh-completionsの設定
fpath=(/usr/local/share/zsh/site-functions(N-/) $fpath)
autoload -Uz compinit && compinit -u

# autoload -Uz add-zsh-hook
autoload -Uz vcs_info


##############################
# ZLE settings
##############################



##############################
# General settings
##############################

setopt auto_list
setopt auto_menu
setopt auto_pushd
setopt extended_history
setopt hist_ignore_all_dups
setopt hist_ignore_dups
setopt hist_reduce_blanks
setopt hist_save_no_dups
setopt ignore_eof
setopt inc_append_history
setopt interactive_comments
setopt no_beep
setopt no_hist_beep
setopt no_list_beep
setopt magic_equal_subst
setopt notify
setopt print_eight_bit
setopt print_exit_value
setopt prompt_subst
setopt pushd_ignore_dups
setopt rm_star_wait
setopt share_history
setopt transient_rprompt


##############################
# Exports
##############################

export CLICOLOR=true
export LSCOLORS='exfxcxdxbxGxDxabagacad'
export LS_COLORS='di=34:ln=35:so=32:pi=33:ex=31:bd=36;01:cd=33;01:su=31;40;07:sg=36;40;07:tw=32;40;07:ow=33;40;07:'
export EDITOR=vim
export HISTFILE=~/.zsh_history
export HISTSIZE=1000000
export SAVEHIST=1000000
export LANG=ja_JP.UTF-8


##############################
# Key bindings
##############################

bindkey -v
bindkey -M viins '^?'  backward-delete-char
bindkey -M viins '^A'  beginning-of-line
bindkey -M viins '^B'  backward-char
bindkey -M viins '^D'  delete-char-or-list
bindkey -M viins '^E'  end-of-line
bindkey -M viins '^F'  forward-char
bindkey -M viins '^G'  send-break
bindkey -M viins '^H'  backward-delete-char
bindkey -M viins '^N'  history-substring-search-down
bindkey -M viins '^P'  history-substring-search-up
bindkey -M viins '^W'  backward-kill-word
bindkey -M viins '^@'  anyframe-widget-cd-ghq-repository


##############################
# Aliases
##############################

alias vi='vim'
alias ll='ls -l'
alias la='ls -a'
alias rm='rmtrash'
alias brew='env PATH=${PATH/\/Users\/${USER}\/\.pyenv\/shims:/} brew'

# anyframe
alias aw='anyframe-widget-select-widget'
alias aweh='anyframe-widget-execute-history'
alias awcgb='anyframe-widget-checkout-git-branch'
alias awcgr='anyframe-widget-cd-ghq-repository'


##############################
# hash
##############################

hash -d dot=~/dotfiles
hash -d hatena=~/Documents/HatenaBlog
hash -d note=~/Documents/Notes
hash -d precision=~/Scripts/Projects/Precision
hash -d kaggle=~/Scripts/DataAnalysis/kaggle
hash -d fbpj=~/Scripts/Projects/FBPJ
hash -d gci=~/Scripts/DataAnalysis/GCI


##############################
# zstyle
##############################

# Completion
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
zstyle ':completion:*' use-cache true
zstyle ':completion:*' verbose yes
zstyle ':completion:*:default' menu select=2
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'
zstyle ':completion:*:options' description 'yes'


##############################
# PATH and environment settings
##############################

export PATH="/usr/bin:/bin:/usr/sbin:/sbin"
export PATH="/usr/local/bin:/usr/local/sbin:$PATH"
export PATH="/usr/local/Cellar/gcc/8.1.0/bin:$PATH"

# pyenv seting
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# nodebrew seting
export PATH=$HOME/.nodebrew/current/bin:$PATH

# Tex setting
export PATH="/Library/TeX/texbin:$PATH"

# react aws setting
source ~/.keys/.zshrc.aws.react

# fbm aws setting
source ~/.keys/.zshrc.aws.fbm

# es setting
source ~/.keys/.zshrc.es

# gcs setting
source ~/.keys/.zshrc.gcs

# tensorflow object detect
export PYTHONPATH=$PYTHONPATH:"/Users/taku/Scripts/FBPJ/tf_obj_det":"/Users/taku/Scripts/FBPJ/tf_obj_det/slim"

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/taku/GoogleCloudSDK/google-cloud-sdk/path.zsh.inc' ]; then source '/Users/taku/GoogleCloudSDK/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/taku/GoogleCloudSDK/google-cloud-sdk/completion.zsh.inc' ]; then source '/Users/taku/GoogleCloudSDK/google-cloud-sdk/completion.zsh.inc'; fi

# exclude waiting time
KEYTIMEOUT=1

##############################
# tmux
##############################
function is_exists() { type "$1" >/dev/null 2>&1; return $?; }
function is_osx() { [[ $OSTYPE == darwin* ]]; }
function is_screen_running() { [ ! -z "$STY" ]; }
function is_tmux_runnning() { [ ! -z "$TMUX" ]; }
function is_screen_or_tmux_running() { is_screen_running || is_tmux_runnning; }
function shell_has_started_interactively() { [ ! -z "$PS1" ]; }
function is_ssh_running() { [ ! -z "$SSH_CONECTION" ]; }

function tmux_automatically_attach_session()
{
    if is_screen_or_tmux_running; then
        ! is_exists 'tmux' && return 1

        if is_tmux_runnning; then
            echo "${fg_bold[red]} _____ __  __ _   ___  __ ${reset_color}"
            echo "${fg_bold[red]}|_   _|  \/  | | | \ \/ / ${reset_color}"
            echo "${fg_bold[red]}  | | | |\/| | | | |\  /  ${reset_color}"
            echo "${fg_bold[red]}  | | | |  | | |_| |/  \  ${reset_color}"
            echo "${fg_bold[red]}  |_| |_|  |_|\___//_/\_\ ${reset_color}"
        elif is_screen_running; then
            echo "This is on screen."
        fi
    else
        if shell_has_started_interactively && ! is_ssh_running; then
            if ! is_exists 'tmux'; then
                echo 'Error: tmux command not found' 2>&1
                return 1
            fi

            if tmux has-session >/dev/null 2>&1 && tmux list-sessions | grep -qE '.*]$'; then
                # detached session exists
                tmux list-sessions
                echo -n "Tmux: attach? (y/N/num) "
                read
                if [[ "$REPLY" =~ ^[Yy]$ ]] || [[ "$REPLY" == '' ]]; then
                    tmux attach-session
                    if [ $? -eq 0 ]; then
                        echo "$(tmux -V) attached session"
                        return 0
                    fi
                elif [[ "$REPLY" =~ ^[0-9]+$ ]]; then
                    tmux attach -t "$REPLY"
                    if [ $? -eq 0 ]; then
                        echo "$(tmux -V) attached session"
                        return 0
                    fi
                fi
            fi

            if is_osx && is_exists 'reattach-to-user-namespace'; then
                # on OS X force tmux's default command
                # to spawn a shell in the user's namespace
                tmux_config=$(cat $HOME/.tmux.conf <(echo 'set-option -g default-command "reattach-to-user-namespace -l $SHELL"'))
                tmux -f <(echo "$tmux_config") new-session && echo "$(tmux -V) created new session supported OS X"
            else
                tmux new-session && echo "tmux created new session"
            fi
        fi
    fi
}
tmux_automatically_attach_session
