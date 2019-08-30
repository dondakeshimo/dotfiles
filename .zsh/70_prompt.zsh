##############################
# Prompt Setting
##############################

# get git information

# $vcs_info_msg_0_ : branch name
# $vcs_info_msg_1_ : status
# $vcs_info_msg_2_ : push, merge, stach status
# $vcs_info_msg_3_ : active status
zstyle ':vcs_info:*' max-exports 4

zstyle ':vcs_info:*' enable git svn hg bzr

# default format
# misc(%m) is empty string
zstyle ':vcs_info:*' formats '%s:%b'
zstyle ':vcs_info:*' actionformats '%s:%b' '%m' '<!%a>'
zstyle ':vcs_info:(svn|bzr):*' branchformat '%b:r%r'
zstyle ':vcs_info:bzr:*' use-simple true

# git format
zstyle ':vcs_info:git:*' formats "%s:%b" '%c%u' '%m'
zstyle ':vcs_info:git:*' actionformats "%s:%b" '%c%u' '%m' '<!%a>'
zstyle ':vcs_info:git:*' check-for-changes true
zstyle ':vcs_info:git:*' stagedstr "%{$fg[yellow]%} uncommitted %{$reset_color%}"    # if all files are staged, it is in %c
zstyle ':vcs_info:git:*' unstagedstr "%{$fg[yellow]%} unstaged %{$reset_color%}"  # if all files are unstaged, it is in %u


# hooks setting
# only git

# formats '(%s)-[%b]' '%c%u %m' , actionformats '(%s)-[%b]' '%c%u %m' '<!%a>'
# this hooks are invoked before setting up formats or actionformats
# each vcs_info_msg_n_ calls hooks, so each function is invoked max three times
#zstyle ':vcs_info:git+set-message:*' hooks \
#                                        git-is-in-dot-git-dir \
#                                        git-untracked \
#                                        git-push-status \
#                                        git-nomerge-branch \
#                                        git-stash-count
zstyle ':vcs_info:git+set-message:*' hooks \
                                        git-is-in-dot-git-dir \
                                        git-untracked \
                                        git-is-clean \
                                        git-status-info

# if you are inside .git directory, hooks are stopped here,
# because some command occure error in .git
# you can stop hooks, if you return anything else 0
+vi-git-is-in-dot-git-dir() {
    if [[ $(command git rev-parse --is-inside-work-tree 2> /dev/null) != 'true' ]]; then
        return 1
    fi

    return 0
}

+vi-git-untracked() {
    if [[ "$1" != "1" ]]; then
        return 0
    fi

    if [[ $(git status 2> /dev/null) =~ "Untracked files:" ]]; then
        hook_com[unstaged]+="%{$fg[red]%} untracked %{$reset_color%}"
    fi
}

+vi-git-is-clean() {
    if [[ "$1" != "1" ]]; then
        return 0
    fi

    if [[ -z "${hook_com[staged]}" && -z "${hook_com[unstaged]}" ]]; then
        hook_com[staged]="%{$fg[green]%} clean %{$reset_color%}"
    fi
}

+vi-git-status-info() {
    if [[ "$1" != "2" ]]; then
        return 0
    fi

    git_status="$(git status 2> /dev/null)"
    hook_com[misc]=""

    git-push-status ${git_status}
    git-diverge-status ${git_status}
}

git-push-status() {
    unpushed_pattern='Your branch is (.*) of (.*) by (.*) commit[s]*\.'
    uptodate_pattern='Your branch is up to date with'
    if [[ "$1" =~ "${unpushed_pattern}" ]]; then
        if [[ ${match[1]} == "ahead" ]]; then
            hook_com[misc]+="%{$fg[yellow]%} ${match[3]} unpushed %{$reset_color%}"
        fi
    elif [[ "$1" =~ "${uptodate_pattern}" ]]; then
        hook_com[misc]+="%{$fg[green]%} uptodate %{$reset_color%}"
    fi
}

git-diverge-status() {
    diverge_pattern='Your branch and (.*) have diverged'
    if [[ "$1" =~ "${diverge_pattern}" ]]; then
        hook_com[misc]+="%{$fg[yellow]%} diverged %{$reset_color%}"
    fi
}

# now no use
+vi-git-nomerge-branch() {
    if [[ "$1" != "2" ]]; then
        return 0
    fi

    if [[ "${hook_com[branch]}" == "master" ]]; then
        return 0
    fi

    local nomerged
    nomerged=$(command git rev-list master..${hook_com[branch]} 2>/dev/null \
        | wc -l \
        | tr -d ' ')

    if [[ "$nomerged" -gt 0 ]] ; then
        hook_com[misc]+=" m:${nomerged} "
    fi
}

# now no use
+vi-git-stash-count() {
    if [[ "$1" != "2" ]]; then
        return 0
    fi

    local stash
    stash=$(command git stash list 2>/dev/null \
        | wc -l \
        | tr -d ' ')

    if [[ "${stash}" -gt 0 ]]; then
        hook_com[misc]+=" s:${stash} "
    fi
}


update-git-prompt() {
    if [[ -z "${vcs_info_msg_0_}" ]]; then
        GIT_PROMPT_INFO="no VCS"
        return 0
    fi

    local git_prompt_info="${vcs_info_msg_0_} "

    if [[ -n "${vcs_info_msg_1_}" ]]; then
        git_prompt_info+=" (${vcs_info_msg_1_}) "
    fi

    if [[ -n "${vcs_info_msg_2_}" ]]; then
        git_prompt_info+=" [${vcs_info_msg_2_}] "
    fi

    git_prompt_info+="${vcs_info_msg_3_}"
    GIT_PROMPT_INFO="${git_prompt_info}"
}


# Prompt format:
#
# For example:
#
#
# % tashimom @ tashimom-MBP [21:47:42] C:0
#     in  ~/.dotfiles
#     on git:master ( + - ? ) [ p:1  m:1  s:1 ]  <!merge>
# $
update-prompt() {
    LANG=en_US.UTF-8 vcs_info

    update-git-prompt
    local exit_code="%(?,C:%{$fg[white]%}%?%{$reset_color%},C:%{$fg[red]%}%?%{$reset_color%})"

    PROMPT="

%{$terminfo[bold]$fg[blue]%}#%{$reset_color%} \
%(#,%{$bg[yellow]%}%{$fg[black]%}%n%{$reset_color%},%{$fg[cyan]%}%n) \
%{$fg[white]%}@ \
%{$fg[green]%}%m \
%{$fg[white]%}[%*] $exit_code
\
    %{$fg[white]%}in %{$terminfo[bold]$fg[yellow]%}%d%{$reset_color%}
\
    %{$fg[white]%}on%{$reset_color%} ${GIT_PROMPT_INFO}
\
%{$terminfo[bold]$fg[red]%}$ %{$reset_color%}"
}


setopt PROMPT_SUBST
add-zsh-hook precmd update-prompt


