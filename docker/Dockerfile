FROM python:3.9

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

WORKDIR /root

RUN echo "Acquire { https::Verify-Peer false }" > /etc/apt/apt.conf.d/99verify-peer.conf \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-unauthenticated ca-certificates \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libopenmpi-dev
# install conda, and the ennvironment. 
RUN curl -o ~/Miniforge3-$(uname)-$(uname -m).sh -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh && \
    bash ~/Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/conda

ENV PATH=/opt/conda/bin:${PATH}
RUN conda update -n base conda && \
    conda install -n base conda-libmamba-solver && \
    conda config --set solver libmamba

RUN conda init bash

## Install spinningup
RUN conda create -n spinningup python=3.7 # 3.7 works with existing setup.py
RUN git clone https://github.com/Juyue/spinningup.git && \
    cd spinningup && \
    conda run -n spinningup pip install -e .
