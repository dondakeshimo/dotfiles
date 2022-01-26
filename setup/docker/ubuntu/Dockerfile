FROM ubuntu:latest

RUN apt-get -y update && \
    apt-get -y install git vim zsh tmux make build-essential wget curl neovim

ARG USERNAME=dondakeshimo
ARG GIT_USER=dondakeshimo
ARG GROUPNAME=user
ARG UID=50001
ARG GID=50001
ARG PASSWORD=password
ARG GIT_TOKEN

RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/zsh -u $UID -g $GID -G sudo $USERNAME && \
    echo $USERNAME:$PASSWORD | chpasswd && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME
WORKDIR /home/$USERNAME/

RUN git clone https://github.com/dondakeshimo/dotfiles.git ~/src/github.com/dondakeshimo/dotfiles && \
    ./src/github.com/dondakeshimo/dotfiles/setup/deployer/symlink.sh bin bash vim nvim git asdf
