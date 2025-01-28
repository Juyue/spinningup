FROM python:3.6

## Add personal settings
ENV LANG=en_US.UTF-8
# Prevent stop building ubuntu at time zone selection.
ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN echo "Acquire { https::Verify-Peer false }" > /etc/apt/apt.conf.d/99verify-peer.conf \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-unauthenticated ca-certificates \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        zsh \
        neovim \
        unzip \
        wget \
        rsync \
        vim \
        ninja-build \
        cmake \
        build-essential \
        xauth \
        openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install fzf
RUN git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && /root/.fzf/install --all

# Install oh-my-zsh and Install Powerlevel10k and zsh-syntax-highlighting
# hadolint ignore=SC2086
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

RUN echo "Acquire { https::Verify-Peer false }" > /etc/apt/apt.conf.d/99verify-peer.conf \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-unauthenticated ca-certificates \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libopenmpi-dev

WORKDIR /root
