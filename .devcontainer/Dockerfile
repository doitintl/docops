ARG VARIANT
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y -q sqlite3

USER vscode
RUN python3 -m pip install --no-cache-dir --no-warn-script-location pipx && \
    python3 -m pipx ensurepath && \
    pipx install poetry
