ARG VARIANT
FROM mcr.microsoft.com/vscode/devcontainers/base:debian as build
ARG VARIANT

# TODO: Switch to using variant-specific `.env` files once the
# `docker/build-push-action@v2` action has been updated to use the latest
# `buildx` release:
#
# - https://github.com/docker/build-push-action/issues/562

# pipx
ENV USE_EMOJI=false
ENV PIPX_HOME=/usr/local/pix
ENV PIPX_BIN_DIR=/usr/local/bin
ENV PATH=$PIPX_BIN_DIR:$PATH

COPY . /tmp/checkout
RUN cd /tmp/checkout && \
  ./bootstrap.sh && \
  make $VARIANT && \
  make clean && \
  rm -rf /tmp/checkout
