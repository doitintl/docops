# =============================================================================
# Build the project
# =============================================================================

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL=C

SUBMAKE=$(MAKE) --no-print-directory

# $(call print-target)
define print-target
@ printf "\e$(BOLD)make %s\e$(RESET)\n" "$$(echo $@ | sed 's,.stamp,,')"
endef

.DEFAULT_GOAL := noop

.PHONY: noop
noop:

# Modules
# =============================================================================

USER := vscode
USER_HOME := /home/$(USER)

DEBIAN_FRONTEND := noninteractive
APT_GET_OPTS := -y --no-install-recommends
APT_GET_INSTALL := apt-get install $(APT_GET_OPTS)

# bashrc
# -----------------------------------------------------------------------------

SRC_BASHRC_DIRCOLORS := src/bashrc/dircolors.sh
SRC_BASHRC_PATH := src/bashrc/path.sh

.PHONY: $(HOME_DIR)/.bashrc
$(USER_HOME)/.bashrc:
	$(call print-target)
	(echo && cat "${SRC_BASHRC_DIRCOLORS}") >>$@
	(echo && cat "${SRC_BASHRC_PATH}") >>$@

.PHONY: bashrc
bashrc: $(HOME_DIR)/.bashrc

# vscode
# -----------------------------------------------------------------------------

VSCODE_CONFIG := $(USER_HOME)/.config/vscode-dev-containers
FIRST_RUN := first-run-notice-already-displayed
VSCODE_FIRST_RUN := $(VSCODE_CONFIG)/$(FIRST_RUN)

# Disable first run notice message
$(VSCODE_FIRST_RUN):
	mkdir -p $(dir $@)
	touch $@

.PHONY: vscode
vscode: $(VSCODE_FIRST_RUN)

# npm
# -----------------------------------------------------------------------------

NPM_INSTALL := npm install -g

.PHONY: npm
npm:
	$(APT_GET_INSTALL) npm
	$(NPM_INSTALL) npm

# python
# -----------------------------------------------------------------------------

PIP_INSTALL := pip install --upgrade
PIPX_INSTALL := pipx install --force

.PHONY: python
python:
	$(APT_GET_INSTALL) python3 python3-pip python3-venv
	$(PIP_INSTALL) pip
	$(PIP_INSTALL) pipx
	$(PIPX_INSTALL) pipx

# poetry
# -----------------------------------------------------------------------------

.PHONY: poetry
poetry: python
	pipx install poetry

# Images
# =============================================================================

# dev
# -----------------------------------------------------------------------------

INSTALL_DEV_APT_PKGS := $(APT_GET_INSTALL) \
	pandoc \
	tidy

INSTALL_DEV_NPM_PKGS := $(NPM_INSTALL) \
	cspell \
	dockerfilelint \
	editorconfig \
	markdownlint-cli \
	prettier \
	shellcheck

.PHONY:
dev:
	$(SUBMAKE) bashrc
	$(SUBMAKE) bashrc USER_HOME=/root
	$(SUBMAKE) vscode
	$(INSTALL_DEV_APT_PKGS)
	$(SUBMAKE) npm
	$(INSTALL_DEV_NPM_PKGS)

# TODO: Install packages from source:
#
# - hadolint
# - lychee
# - shfmt
# - woke

# dev-python
# -----------------------------------------------------------------------------

.PHONY: dev-python
dev-python: dev
	$(SUBMAKE) poetry

# clean
# -----------------------------------------------------------------------------

.PHONY: clean-apt
clean-apt:
	apt-get clean
	apt-get auto-remove
	rm -rf /var/lib/apt/lists/*

.PHONY: clean-npm
clean-npm:
	npm dedupe
	npm prune
	npm cache clean --force

.PHONY: clean
clean: clean-apt clean-npm
