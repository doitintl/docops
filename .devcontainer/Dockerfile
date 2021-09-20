FROM mcr.microsoft.com/vscode/devcontainers/base:0-buster

ARG INSTALL_ZSH="false"
ARG UPGRADE_PACKAGES="true"
ARG ENABLE_NONROOT_DOCKER="true"
ARG USE_MOBY="true"

# Install needed packages and setup non-root user. Use a separate RUN statement
# to add your own dependencies. A user of "automatic" attempts to reuse an user
# ID if one already exists.
ARG USERNAME=automatic
ARG USER_UID=1000
ARG USER_GID=$USER_UID
COPY library-scripts/*.sh /tmp/library-scripts/
RUN apt-get update \
  && /bin/bash /tmp/library-scripts/common-debian.sh \
  "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" \
  "${UPGRADE_PACKAGES}" "true" "true" \
  && /bin/bash /tmp/library-scripts/docker-in-docker-debian.sh \
  "${ENABLE_NONROOT_DOCKER}" "${USERNAME}" "${USE_MOBY}" \
  # Clean up
  && apt-get autoremove -y && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/* /tmp/library-scripts/

VOLUME [ "/var/lib/docker" ]

# Setting the `ENTRYPOINT` to the `docker-init.sh` script  will start up the
# Docker Engine inside the container
ENTRYPOINT [ "/usr/local/share/docker-init.sh" ]
# You can alter the script arguments if you need to change startup behavior
CMD [ "sleep", "infinity" ]
