# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal dotfiles repository for managing development environment configurations across different machines. It uses a symlink-based deployment system to manage configurations for various tools including zsh, vim/neovim, tmux, git, and platform-specific tools like Alacritty and Aerospace.

## Common Commands

### Deployment Commands

The primary deployment mechanism uses the symlink script located at `setup/deployer/symlink.sh`:

```bash
# Deploy all configurations (dotfiles + binaries)
./setup/deployer/symlink.sh all

# Deploy specific components
./setup/deployer/symlink.sh dotfiles  # All dotfiles
./setup/deployer/symlink.sh zsh       # Only zsh configurations
./setup/deployer/symlink.sh vim       # Only vim configurations
./setup/deployer/symlink.sh config    # Only .config directory
./setup/deployer/symlink.sh tmux      # Only tmux configuration
./setup/deployer/symlink.sh git       # Only git configurations
./setup/deployer/symlink.sh bin       # Only binary tools
```

### Testing Commands

To verify configurations after deployment:
```bash
source $HOME/.bash_profile  # Test bash configuration
vim .vimrc                  # Test vim with a file
nvim .vimrc                 # Test neovim with a file
tmux new -s test -d         # Test tmux by creating a session
```

### Installation (Fresh Systems)

For initial setup on new machines:
```bash
# macOS (including M1)
bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/entrypoint/mac_full.sh)"

# Linux (apt-based)
bash -c "$(curl -L raw.githubusercontent.com/dondakeshimo/dotfiles/master/setup/entrypoint/apt_full.sh)"
```

## Architecture and Structure

### Directory Organization

- **Root Level**: Primary dotfiles (`.zshrc`, `.vimrc`, `.tmux.conf`, `.gitconfig`, etc.)
- **`.zsh/`**: Modular zsh configuration files loaded in numerical order
- **`.config/`**: Application-specific configurations (nvim, alacritty, aerospace, karabiner)
- **`bin/`**: Custom scripts and tools, with OS-specific subdirectories (darwin, linux)
- **`setup/`**: Installation and deployment scripts
  - `entrypoint/`: Platform-specific installation scripts
  - `deployer/`: Symlink deployment script
  - `installer/`: Component installation scripts

### Deployment Mechanism

The repository uses symlinks to deploy configurations. The `symlink.sh` script:
1. Creates symlinks from repository files to their expected locations in `$HOME`
2. Backs up existing files before creating symlinks
3. Supports selective deployment of specific components
4. Handles both individual files and entire directories

### Configuration Loading Order

Zsh configurations in `.zsh/` are loaded in numerical order:
- `00_zshenv.zsh`: Environment variables
- `10_common.zsh`: Common shell configurations
- `50_*`: Tool-specific configurations (asdf, git, google cloud, etc.)
- `70_*`: Development environment setups (golang, nodejs, python, ruby)
- `80_*`: Additional tools (fzf, vim)
- `99_*`: Final configurations (aliases)

### Platform Support

The repository supports three deployment scenarios:
1. **Main Machine**: Full GUI environment with all tools
2. **Development Machine**: Rich CLI environment for SSH access
3. **Verification Machine**: Minimal setup with just vim and git

### CI/CD

GitHub Actions workflow (`.github/workflows/test.yml`) tests deployment on:
- macOS (latest)
- Ubuntu (latest)

The workflow verifies that all configurations can be successfully deployed and basic commands work.

## Development Conventions

- **Binary Path**: Custom scripts should be placed in `~/bin` (managed by this repository)
- **Repository Path**: This repository should be cloned to `~/src/github.com/dondakeshimo/dotfiles`
- **Symlink Updates**: Changes to files in the repository are immediately reflected in the system due to symlinks
- **Testing Changes**: After modifying configurations, test them directly without redeployment (changes are live via symlinks)

## Notes on Modifications

When modifying this repository:
1. Test changes locally before committing
2. For new dotfiles, add them to the appropriate section in `symlink.sh`
3. For new zsh modules, follow the numerical naming convention in `.zsh/`
4. Platform-specific scripts go in `bin/darwin/` or `bin/linux/`
5. Update installation scripts if adding new dependencies