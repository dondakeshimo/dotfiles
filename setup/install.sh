#!/bin/bash

####################
#                  #
#  Util functions  #
#                  #
####################

# PLATFORM is the environment variable that
# retrieves the name of the running platform
export PLATFORM


# ostype returns the lowercase OS name
ostype() {
    # shellcheck disable=SC2119
    uname | lower
}


# os_detect export the PLATFORM variable as you see fit
os_detect() {
    export PLATFORM
    case "$(ostype)" in
        *'linux'*)  PLATFORM='linux'   ;;
        *'darwin'*) PLATFORM='osx'     ;;
        *'bsd'*)    PLATFORM='bsd'     ;;
        *)          PLATFORM='unknown' ;;
    esac
}


# is_osx returns true if running OS is Macintosh
is_osx() {
    os_detect
    if [ "$PLATFORM" = "osx" ]; then
        return 0
    else
        return 1
    fi
}
alias is_mac=is_osx


# is_linux returns true if running OS is GNU/Linux
is_linux() {
    os_detect
    if [ "$PLATFORM" = "linux" ]; then
        return 0
    else
        return 1
    fi
}


# is_bsd returns true if running OS is FreeBSD
is_bsd() {
    os_detect
    if [ "$PLATFORM" = "bsd" ]; then
        return 0
    else
        return 1
    fi
}


# get_os returns OS name of the platform that is running
get_os() {
    local os
    for os in osx linux bsd; do
        if is_$os; then
            echo $os
        fi
    done
}


e_newline() {
    printf "\n"
}


e_header() {
    printf " \033[37;1m%s\033[m\n" "$*"
}


e_error() {
    printf " \033[31m%s\033[m\n" "✖ $*" 1>&2
}


e_warning() {
    printf " \033[31m%s\033[m\n" "$*"
}


e_done() {
    printf " \033[37;1m%s\033[m...\033[32mOK\033[m\n" "✔ $*"
}


e_arrow() {
    printf " \033[37;1m%s\033[m\n" "➜ $*"
}


e_indent() {
    for ((i=0; i<${1:-4}; i++)); do
        echon " "
    done
    if [ -n "$2" ]; then
        echo "$2"
    else
        cat <&0
    fi
}


e_success() {
    printf " \033[37;1m%s\033[m%s...\033[32mOK\033[m\n" "✔ " "$*"
}


e_failure() {
    die "${1:-$FUNCNAME}"
}


ink() {
    if [ "$#" -eq 0 -o "$#" -gt 2 ]; then
        echo "Usage: ink <color> <text>"
        echo "Colors:"
        echo "  black, white, red, green, yellow, blue, purple, cyan, gray"
        return 1
    fi

    local open="\033["
    local close="${open}0m"
    local black="0;30m"
    local red="1;31m"
    local green="1;32m"
    local yellow="1;33m"
    local blue="1;34m"
    local purple="1;35m"
    local cyan="1;36m"
    local gray="0;37m"
    local white="$close"

    local text="$1"
    local color="$close"

    if [ "$#" -eq 2 ]; then
        text="$2"
        case "$1" in
            black | red | green | yellow | blue | purple | cyan | gray | white)
            eval color="\$$1"
            ;;
        esac
    fi

    printf "${open}${color}${text}${close}"
}


logging() {
    if [ "$#" -eq 0 -o "$#" -gt 2 ]; then
        echo "Usage: ink <fmt> <msg>"
        echo "Formatting Options:"
        echo "  TITLE, ERROR, WARN, INFO, SUCCESS"
        return 1
    fi

    local color=
    local text="$2"

    case "$1" in
        TITLE)
            color=yellow
            ;;
        ERROR | WARN)
            color=red
            ;;
        INFO)
            color=blue
            ;;
        SUCCESS)
            color=green
            ;;
        *)
            text="$1"
    esac

    timestamp() {
        ink gray "["
        ink purple "$(date +%H:%M:%S)"
        ink gray "] "
    }

    timestamp; ink "$color" "$text"; echo
}


log_pass() {
    logging SUCCESS "$1"
}


log_fail() {
    logging ERROR "$1" 1>&2
}


log_fail() {
    logging WARN "$1"
}


log_info() {
    logging INFO "$1"
}


log_echo() {
    logging TITLE "$1"
}


# is_exists returns true if executable $1 exists in $PATH
is_exists() {
    which "$1" >/dev/null 2>&1
    return $?
}


# die returns exit code error and echo error message
die() {
    e_error "$1" 1>&2
    exit "${2:-1}"
}


# is_login_shell returns true if current shell is first shell
is_login_shell() {
    [ "$SHLVL" = 1 ]
}


# is_git_repo returns true if cwd is in git repository
is_git_repo() {
    git rev-parse --is-inside-work-tree &>/dev/null
    return $?
}


# is_screen_running returns true if GNU screen is running
is_screen_running() {
    [ ! -z "$STY" ]
}


# is_tmux_runnning returns true if tmux is running
is_tmux_runnning() {
    [ ! -z "$TMUX" ]
}


# is_screen_or_tmux_running returns true if GNU screen or tmux is running
is_screen_or_tmux_running() {
    is_screen_running || is_tmux_runnning
}


# shell_has_started_interactively returns true if the current shell is
# running from command line
shell_has_started_interactively() {
    [ ! -z "$PS1" ]
}


# is_ssh_running returns true if the ssh deamon is available
is_ssh_running() {
    [ ! -z "$SSH_CLIENT" ]
}


# is_debug returns true if $DEBUG is set
is_debug() {
    if [ "$DEBUG" = 1 ]; then
        return 0
    else
        return 1
    fi
}


# is_number returns true if $1 is int type
is_number() {
    if [ $# -eq 0 ]; then
        cat <&0
    else
        echo "$1"
    fi | grep -E '^[0-9]+$' >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        return 0
    else
        return 1
    fi
}
alias is_int=is_number
alias is_num=is_number


# echon is a script to emulate the -n flag functionality with 'echo'
# for Unix systems that don't have that available.
echon() {
    echo "$*" | tr -d '\n'
}


# lower returns a copy of the string with all letters mapped to their lower case.
# shellcheck disable=SC2120
lower() {
    if [ $# -eq 0 ]; then
        cat <&0
    elif [ $# -eq 1 ]; then
        if [ -f "$1" -a -r "$1" ]; then
            cat "$1"
        else
            echo "$1"
        fi
    else
        return 1
    fi | tr "[:upper:]" "[:lower:]"
}


# upper returns a copy of the string with all letters mapped to their upper case.
# shellcheck disable=SC2120
upper() {
    if [ $# -eq 0 ]; then
        cat <&0
    elif [ $# -eq 1 ]; then
        if [ -f "$1" -a -r "$1" ]; then
            cat "$1"
        else
            echo "$1"
        fi
    else
        return 1
    fi | tr "[:lower:]" "[:upper:]"
}


#######################
#                     #
#  Process functions  #
#                     #
#######################


# Set DOTPATH as default variable
if [ -z "${DOTPATH:-}" ]; then
    DOTPATH=~/Scripts/src/github.com/dondakeshimo/dotfiles; export DOTPATH
fi

DOTFILES_GITHUB="https://github.com/dondakeshimo/dotfiles.git"; export DOTFILES_GITHUB

# shellcheck disable=SC1078,SC1079,SC2016
dotfiles_logo='

       __                __      __             __    _               
  ____/ /___  ____  ____/ /___ _/ /_____  _____/ /_  (_)___ ___  ____ 
 / __  / __ \/ __ \/ __  / __ `/ //_/ _ \/ ___/ __ \/ / __ `__ \/ __ \
/ /_/ / /_/ / / / / /_/ / /_/ / ,< /  __(__  ) / / / / / / / / / /_/ /
\__,_/\____/_/ /_/\__,_/\__,_/_/|_|\___/____/_/ /_/_/_/ /_/ /_/\____/ 

'


dotfiles_download() {
    if [ -d "$DOTPATH" ]; then
        log_fail "$DOTPATH: already exists"
        exit 1
    fi

    e_newline
    e_header "Downloading dotfiles..."

    if is_debug; then
        :
    else
        if is_exists "git"; then
            # --recursive equals to ...
            # git submodule init
            # git submodule update
            git clone --recursive "$DOTFILES_GITHUB" "$DOTPATH"
        else
            log_fail "git required"
            exit 1
        fi
    fi &&

        e_newline && e_done "Download"
}


dotfiles_deploy() {
    e_newline
    e_header "Deploying dotfiles..."

    if [ ! -d $DOTPATH ]; then
        log_fail "$DOTPATH: not found"
        exit 1
    fi

    if is_debug; then
        :
    else
        cd "$DOTPATH/setup"
        if [ -f symlink.sh ]; then
            bash ./symlink.sh
        else
            log_fail "$DOTPATH/setup/symlink.sh: not found"
            exit 1
        fi
    fi &&

        e_newline && e_done "Deploy"
}


dotfiles_initialize() {
    if [ "$1" = "init" ]; then
        e_newline
        e_header "Initializing dotfiles..."

        if is_debug; then
            :
        else
            cd "$DOTPATH/setup"
            if [ -f init.sh ]; then
                bash ./init.sh
            else
                log_fail "$DOTPATH/setup/init.sh: not found"
                exit 1
            fi
        fi &&

            e_newline && e_done "Initialize"
    fi
}


# A script for the file named "install"
dotfiles_install() {
    # 1. Download the repository
    # ==> downloading
    dotfiles_download &&

    # 2. Deploy dotfiles to your home directory
    # ==> deploying
    dotfiles_deploy &&

    # 3. Execute all sh files within etc/init/
    # ==> initializing
    dotfiles_initialize "$@"
}


if echo "$-" | grep -q "i"; then
    # -> source a.sh
    VITALIZED=1
    export VITALIZED

    : return
else
    # three patterns
    # -> cat a.sh | bash
    # -> bash -c "$(cat a.sh)"
    # -> bash a.sh

    # -> bash a.sh
    if [ "$0" = "${BASH_SOURCE:-}" ]; then
        exit
    fi

    # -> cat a.sh | bash
    # -> bash -c "$(cat a.sh)"
    if [ -n "${BASH_EXECUTION_STRING:-}" ] || [ -p /dev/stdin ]; then
        # if already vitalized, skip to run dotfiles_install
        if [ "${VITALIZED:=0}" = 1 ]; then
            exit
        fi

        trap "e_error 'terminated'; exit 1" INT ERR
        echo "$dotfiles_logo"
        dotfiles_install "$@"

        # Restart shell if specified "bash -c $(curl -L {URL})"
        # not restart:
        #   curl -L {URL} | bash
        if [ -p /dev/stdin ]; then
            e_warning "Now continue with Rebooting your shell"
        else
            e_newline
            e_arrow "Restarting your shell..."
            exec "${SHELL:-/bin/zsh}"
        fi
    fi
fi

# __END__ {{{1
# vim:fdm=marker
