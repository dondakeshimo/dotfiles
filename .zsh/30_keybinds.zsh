##############################
# Key bindings
##############################

# vim keybind
bindkey -v

# delete key
bindkey -M viins '^?'  backward-delete-char

# cursor key bind like emacs
bindkey -M viins '^A'  beginning-of-line
bindkey -M viins '^B'  backward-char
bindkey -M viins '^D'  delete-char-or-list
bindkey -M viins '^E'  end-of-line
bindkey -M viins '^F'  forward-char
bindkey -M viins '^G'  send-break
bindkey -M viins '^H'  backward-delete-char
bindkey -M viins '^W'  backward-kill-word

# history substring
bindkey -M viins '^N'  history-substring-search-down
bindkey -M viins '^P'  history-substring-search-up

# history with interactive search
bindkey -M viins '^@'  anyframe-widget-put-history
