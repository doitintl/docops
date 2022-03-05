# Update timestamp to force a rebuild
# 1633294371968

FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu as build

ARG DEBIAN_FRONTEND=noninteractive
# https://github.com/hadolint/hadolint/wiki/DL3008
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    apt-get auto-remove && \
    rm -rf /var/lib/apt/lists/*

# TODO: Move the whole build script into the Dockerfile
# If we do this, we can take advantage of hadolint's warnings
COPY build /tmp/build
USER vscode
RUN /tmp/build/run/vscode.sh
USER root
RUN rm -rf /tmp/build
USER vscode

FROM scratch
COPY --from=build / /
