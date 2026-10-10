##############################
# Set sheldon
##############################
# Config: ~/.config/sheldon/plugins.toml (deployed by setup/deployer/symlink.sh)
# Docs:   https://sheldon.cli.rs

if command -v sheldon >/dev/null 2>&1; then
    eval "$(sheldon source)"
fi
