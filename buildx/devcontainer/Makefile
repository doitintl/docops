# =============================================================================
# Prepare the container image
# =============================================================================

# This Makefile is copied into the container image by the Dockerfile

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

SRC_DIR := $(subst /,,$(dir $(lastword $(MAKEFILE_LIST))))
TEMPLATES_DIR := templates
TMP_DIR := tmp

ROOT = root
USER = vscode

ROOT_HOME = /$(ROOT)
USER_HOME = /home/$(USER)
USER_LOCAL = $(USER_HOME)/.local
SYSTEM_LOCAL = /usr/local
SYSTEM_BIN = $(SYSTEM_LOCAL)/bin

CURL = curl -fsSL
UNTGZ = tar -xzf

GH_BASE = https://github.com
GH_DOWNLOAD = releases/download
GH_LATEST = releases/latest

# Primary targets
# =============================================================================

.DEFAULT_GOAL = help

.PHONY: help
help:
	@ printf '%s\n\n' "Usage: make [target]"
	@ printf '%s\n\n' 'Available targets:'
	@ grep -E '^.PHONY: [a-z]+ #' Makefile | \
		sed -E 's,^.PHONY: ([a-z]+) # (.*),\1#\2,' | \
		column -s '#' -t | \
		sed -E "s,^([a-z]+),  \1,"

.PHONY: build # Install and configure software packages
build:

.PHONY: clean # Remove build artifacts
clean:
	rm -rf $(TMP_DIR)

# Functions
# =============================================================================

# gh_get_latest
# -----------------------------------------------------------------------------

# $(call gh_get_latest,repo)
define gh_get_latest
@ curl -sI '$(GH_BASE)/$(1)/$(GH_LATEST)' | \
	grep '^location' | sed 's,.*: ,,'
endef

# gh_test_latest
# -----------------------------------------------------------------------------

# $(call gh_test_latest,repo,tag)
define gh_test_latest
$(call gh_get_latest,$(1)) | tee -- $@.latest
@ if ! cat <$@.latest | grep -F '$(2)' >/dev/null; then \
	echo 'ERROR: Version mismatch'; \
	exit 1; \
fi
@ rm -- $@.latest
endef

# gh_url
# -----------------------------------------------------------------------------

# $(call gh_url,repo,tag,file)
define gh_url
$(strip $(GH_BASE)/$(strip $(1))/$(GH_DOWNLOAD)/$(strip $(2))/$(strip $(3)))
endef

# reset_dir
# -----------------------------------------------------------------------------

# $(call reset_dir,dir)
define reset_dir
rm -rf $(1) && mkdir -p $(1)
endef

# install_bin
# -----------------------------------------------------------------------------

# $(call install_bin,file)
define install_bin
chown -R root:root $(1) && \
chmod -R 755 $(1) && \
mv $(1) $(SYSTEM_BIN)
endef

# Primary target dependencies
# =============================================================================

# black
# -----------------------------------------------------------------------------

# Black
# https://github.com/psf/black

.PHONY: black
black: pipx-black
build: black

# brok
# -----------------------------------------------------------------------------

# https://github.com/smallhadroncollider/brok

BROK_PKG = brok
BROK_DIR = $(TMP_DIR)/$(BROK_PKG)
BROK_VERSION = 1.1.0
BROK_REPO = smallhadroncollider/brok
BROK_DEB = $(BROK_PKG)-$(BROK_VERSION)_x86-64-linux.deb
BROK_DEB_URL = $(call gh_url,$(BROK_REPO),$(BROK_VERSION),$(BROK_DEB))

.PHONY: brok
brok:
	$(call gh_test_latest,$(BROK_REPO),$(BROK_VERSION))
	$(call reset_dir,$(BROK_DIR))
	$(CURL) $(BROK_DEB_URL) >$(BROK_DIR)/$(BROK_DEB)
	dpkg -i $(BROK_DIR)/$(BROK_DEB)
	rm -rf $(BROK_DIR)
build: brok

# build-essential
# -----------------------------------------------------------------------------

# build-essential
# https://packages.debian.org/bullseye/build-essential

.PHONY: build-essential
build-essential: apt-build-essential
build: build-essential

# codespell
# -----------------------------------------------------------------------------

# codespell
# https://github.com/codespell-project/codespell

.PHONY: codespell
codespell: pipx-codespell
build: codespell

# cspell
# -----------------------------------------------------------------------------

# cspell
# https://github.com/streetsidesoftware/cspell

.PHONY: cspell
cspell: npm-cspell
build: cspell

# dockerfilelint
# -----------------------------------------------------------------------------

# https://github.com/replicatedhq/dockerfilelint

.PHONY: dockerfilelint
dockerfilelint: npm-dockerfilelint
build: dockerfilelint

# doitintl-docops
# -----------------------------------------------------------------------------

# https://github.com/doitintl/docops-cli

.PHONY: doitintl-docops
doitintl-docops: pipx-doitintl-docops
build: doitintl-docops

# dotfiles
# -----------------------------------------------------------------------------

BASHRC_SRC = $(TEMPLATES_DIR)/bashrc.sh

BASHRC_DEST = .bash_docops
CONFIG_DIR = .config
VSCODE_DEV_CONTAINERS_DIR = $(CONFIG_DIR)/vscode-dev-containers
FIRST_RUN = $(VSCODE_DEV_CONTAINERS_DIR)/first-run-notice-already-displayed
PARALLEL_DIR = .parallel
WILL_CITE = $(PARALLEL_DIR)/will-cite

# $(call mkdir,user,dir)
define mkdir
mkdir -p $(2)
chown -R $(1):$(1) $(2)
endef

# $(call touch,user,file)
define touch
touch $(2)
chown -R $(1):$(1) $(2)
endef

# $(call install_bashrc,user,home)
define install_bashrc
cp $(BASHRC_SRC) $(2)/$(BASHRC_DEST)
chown $(1):$(1) $(2)/$(BASHRC_DEST)
sed -i '/^.*$(BASHRC_DEST)$$/d' $(2)/.bashrc
printf '\n. ~/$(BASHRC_DEST)\n' >>$(2)/.bashrc
gawk -i inplace 'NF{c=1} (c++)<3' $(2)/.bashrc
endef

.PHONY: dotfiles
dotfiles: apt-bash-completion apt-gawk
	$(call install_bashrc,$(ROOT),$(ROOT_HOME))
	$(call mkdir,$(ROOT),$(ROOT_HOME)/$(PARALLEL_DIR))
	$(call touch,$(ROOT),$(ROOT_HOME)/$(WILL_CITE))
	$(call install_bashrc,$(USER),$(USER_HOME))
	$(call mkdir,$(USER),$(USER_HOME)/$(PARALLEL_DIR))
	$(call touch,$(USER),$(USER_HOME)/$(WILL_CITE))
	$(call mkdir,$(USER),$(USER_HOME)/$(CONFIG_DIR))
	$(call mkdir,$(USER),$(USER_HOME)/$(VSCODE_DEV_CONTAINERS_DIR))
	$(call touch,$(USER),$(USER_HOME)/$(FIRST_RUN))
build: dotfiles

# ec
# -----------------------------------------------------------------------------

# https://github.com/editorconfig-checker/editorconfig-checker

EC_BIN = ec
EC_DIR = $(TMP_DIR)/$(EC_BIN)
EC_VERSION = 2.4.0
EC_REPO = editorconfig-checker/editorconfig-checker
EC_FILE = $(EC_BIN)-linux-amd64
EC_TGZ = $(EC_FILE).tar.gz
EC_URL = $(call gh_url,$(EC_REPO),$(EC_VERSION),$(EC_TGZ))

# TODO: Create temporary directory

.PHONY: ec
ec:
	$(call gh_test_latest,$(EC_REPO),$(EC_VERSION))
	$(call reset_dir,$(EC_DIR))
	$(CURL) $(EC_URL) >$(EC_DIR)/$(EC_TGZ)
	cd $(EC_DIR) && $(UNTGZ) $(EC_TGZ)
	cd $(EC_DIR) && mv bin/$(EC_FILE) $(EC_BIN)
	cd $(EC_DIR) && $(call install_bin,$(EC_BIN))
	rm -rf $(EC_DIR)
build: ec

# fd-find
# -----------------------------------------------------------------------------

# https://github.com/sharkdp/fd

.PHONY: fd-find
fd-find: apt-fd-find
build: fd-find

# fdupes
# -----------------------------------------------------------------------------

# https://github.com/adrianlopezroche/fdupes

.PHONY: fdupes
fdupes: apt-fdupes
build: fdupes

# file
# -----------------------------------------------------------------------------

# https://github.com/file/file

.PHONY: file
file: apt-file
build: file

# fixred
# -----------------------------------------------------------------------------

# https://github.com/rhysd/fixred

# Disabled until I can figure out a way to build this software:
# https://github.com/rhysd/fixred/issues/1

# .PHONY: fixred
# fixred: cargo-fixred

# hadolint
# -----------------------------------------------------------------------------

# https://github.com/hadolint/hadolint

HADOLINT_BIN = hadolint
HADOLINT_DIR = $(TMP_DIR)/$(HADOLINT_BIN)
HADOLINT_VERSION = 2.10.0
HADOLINT_REPO = hadolint/hadolint
HADOLINT_FILE = $(HADOLINT_BIN)-Linux-x86_64
HADOLINT_FILE_URL = $(call gh_url, \
	$(HADOLINT_REPO),v$(HADOLINT_VERSION),$(HADOLINT_FILE))

.PHONY: hadolint
hadolint:
	$(call gh_test_latest,$(HADOLINT_REPO),v$(HADOLINT_VERSION))
	$(call reset_dir,$(HADOLINT_DIR))
	$(CURL) $(HADOLINT_FILE_URL) >$(HADOLINT_DIR)/$(HADOLINT_BIN)
	$(call install_bin,$(HADOLINT_DIR)/$(HADOLINT_BIN))
	rm -rf $(HADOLINT_DIR)
build: hadolint

# html-minifier
# -----------------------------------------------------------------------------

# https://github.com/kangax/html-minifier

.PHONY: html-minifier
html-minifier: npm-html-minifier
build: html-minifier

# imagemagick
# -----------------------------------------------------------------------------

# https://github.com/ImageMagick/ImageMagick

.PHONY: imagemagick
imagemagick: apt-imagemagick
build: imagemagick

# imgdup2go
# -----------------------------------------------------------------------------

# https://github.com/rif/imgdup2go

IMGDUP2GO_BIN = imgdup2go
IMGDUP2GO_DIR = $(TMP_DIR)/$(IMGDUP2GO_BIN)
IMGDUP2GO_VERSION = 2.1.0
IMGDUP2GO_REPO = rif/imgdup2go
IMGDUP2GO_TGZ = $(IMGDUP2GO_BIN)_$(IMGDUP2GO_VERSION)_linux_386.tar.gz
IMGDUP2GO_TGZ_URL = $(call gh_url, \
	$(IMGDUP2GO_REPO),v$(IMGDUP2GO_VERSION),$(IMGDUP2GO_TGZ))

.PHONY: imgdup2go
imgdup2go:
	$(call gh_test_latest,$(IMGDUP2GO_REPO),v$(IMGDUP2GO_VERSION))
	$(call reset_dir,$(IMGDUP2GO_DIR))
	$(CURL) $(IMGDUP2GO_TGZ_URL) >$(IMGDUP2GO_DIR)/$(IMGDUP2GO_TGZ)
	cd $(IMGDUP2GO_DIR) && $(UNTGZ) $(IMGDUP2GO_TGZ)
	cd $(IMGDUP2GO_DIR) && $(call install_bin,$(IMGDUP2GO_BIN))
	rm -rf $(IMGDUP2GO_DIR)
build: imgdup2go

# lintspaces-cli
# -----------------------------------------------------------------------------

# https://github.com/evanshortiss/lintspaces-cli

.PHONY: lintspaces-cli
lintspaces-cli: npm-lintspaces-cli
build: lintspaces-cli

# markdown-link-check
# -----------------------------------------------------------------------------

# https://github.com/tcort/markdown-link-check

.PHONY: markdown-link-check
markdown-link-check: npm-markdown-link-check
build: markdown-link-check

# markdownlint-cli
# -----------------------------------------------------------------------------

# https://github.com/igorshubovych/markdownlint-cli

.PHONY: markdownlint-cli
markdownlint-cli: npm-markdownlint-cli
build: markdownlint-cli

# misspell
# -----------------------------------------------------------------------------

# https://github.com/client9/misspell

MISSPELL_BIN = misspell
MISSPELL_DIR = $(TMP_DIR)/$(MISSPELL_BIN)
MISSPELL_VERSION = 0.3.4
MISSPELL_REPO = client9/misspell
MISSPELL_TGZ = $(MISSPELL_BIN)_$(MISSPELL_VERSION)_linux_64bit.tar.gz
MISSPELL_TGZ_URL = $(call gh_url, \
	$(MISSPELL_REPO),v$(MISSPELL_VERSION),$(MISSPELL_TGZ))

.PHONY: misspell
misspell:
	$(call gh_test_latest,$(MISSPELL_REPO),v$(MISSPELL_VERSION))
	$(call reset_dir,$(MISSPELL_DIR))
	$(CURL) $(MISSPELL_TGZ_URL) >$(MISSPELL_DIR)/$(MISSPELL_TGZ)
	cd $(MISSPELL_DIR) && $(UNTGZ) $(MISSPELL_TGZ)
	cd $(MISSPELL_DIR) && $(call install_bin,$(MISSPELL_BIN))
	rm -rf $(MISSPELL_DIR)
build: misspell

# moreutils
# -----------------------------------------------------------------------------

# https://joeyh.name/code/moreutils/

.PHONY: moreutils
imagemagick: apt-moreutils
build: moreutils

# optipng
# -----------------------------------------------------------------------------

# https://github.com/johnpaulada/optipng

.PHONY: optipng
optipng: apt-optipng
build: optipng

# pandoc
# -----------------------------------------------------------------------------

# https://github.com/jgm/pandoc

.PHONY: pandoc
pandoc: apt-pandoc
build: pandoc

# parallel
# -----------------------------------------------------------------------------

# https://github.com/martinda/gnu-parallel

.PHONY: parallel
parallel: apt-parallel
build: parallel

# poetry
# -----------------------------------------------------------------------------

# https://github.com/python-poetry/poetry

.PHONY: poetry
poetry: pipx-poetry
build: poetry

# prettier
# -----------------------------------------------------------------------------

# https://github.com/prettier/prettier

.PHONY: prettier
prettier: npm-prettier
prettier: npm-prettier-plugin-toml
build: prettier

# proselint
# -----------------------------------------------------------------------------

# https://github.com/amperser/proselint

# TODO: Retire this package in favour of the proselint textlint plugin (which
# supports line-by-line disabling)

.PHONY: proselint
proselint: npm-proselint pipx-proselint
build: proselint

# shellcheck
# -----------------------------------------------------------------------------

# https://github.com/koalaman/shellcheck

.PHONY: shellcheck
shellcheck: apt-shellcheck
build: shellcheck

# shfmt
# -----------------------------------------------------------------------------

# https://github.com/mvdan/sh#shfmt

SHFMT_BIN = shfmt
SHFMT_DIR = $(TMP_DIR)/$(SHFMT_BIN)
SHFMT_VERSION = 3.5.0
SHFMT_REPO = mvdan/sh
SHFMT_FILE = $(SHFMT_BIN)_v$(SHFMT_VERSION)_linux_amd64
SHFMT_FILE_URL = $(call gh_url, \
	$(SHFMT_REPO),v$(SHFMT_VERSION),$(SHFMT_FILE))

.PHONY: shfmt
shfmt:
	$(call gh_test_latest,$(SHFMT_REPO),v$(SHFMT_VERSION))
	$(call reset_dir,$(SHFMT_DIR))
	$(CURL) $(SHFMT_FILE_URL) >$(SHFMT_DIR)/$(SHFMT_BIN)
	$(call install_bin,$(SHFMT_DIR)/$(SHFMT_BIN))
	rm -rf $(SHFMT_DIR)
build: shfmt

# silversearcher-ag
# -----------------------------------------------------------------------------

# https://github.com/ggreer/the_silver_searcher

.PHONY: silversearcher-ag
silversearcher-ag: apt-silversearcher-ag
build: silversearcher-ag

# textlint
# -----------------------------------------------------------------------------

# https://github.com/textlint/textlint

TEXTLINT_DEPS = \
	npm-dictionary-en \
	npm-textlint \
	npm-textlint-filter-rule-allowlist \
	npm-textlint-filter-rule-comments \
	npm-textlint-filter-rule-node-types \
	npm-textlint-rule-abbr-within-parentheses \
	npm-textlint-rule-alex \
	npm-textlint-rule-apostrophe \
	npm-textlint-rule-common-misspellings \
	npm-textlint-rule-diacritics \
	npm-textlint-rule-doubled-spaces \
	npm-textlint-rule-en-capitalization \
	npm-textlint-rule-en-max-word-count \
	npm-textlint-rule-en-spell \
	npm-textlint-rule-max-comma \
	npm-textlint-rule-no-dead-link \
	npm-textlint-rule-no-empty-section \
	npm-textlint-rule-no-start-duplicated-conjunction \
	npm-textlint-rule-no-todo \
	npm-textlint-rule-no-zero-width-spaces \
	npm-textlint-rule-rousseau \
	npm-textlint-rule-spelling \
	npm-textlint-rule-stop-words \
	npm-textlint-rule-terminology \
	npm-textlint-rule-unexpanded-acronym \
	npm-textlint-rule-write-good \

.PHONY: textlint
textlint: $(TEXTLINT_DEPS) npm pipx-proselint
	@ # Install manually because the `@` doesn't work as a pattern rule
	$(NPM_INSTALL) \
		@textlint-rule/textlint-rule-no-duplicate-abbr \
		@textlint-rule/textlint-rule-no-invalid-control-character \
		@textlint-rule/textlint-rule-no-unmatched-pair \
		@textlint-rule/textlint-rule-proselint
build: textlint

# tidy
# -----------------------------------------------------------------------------

# https://github.com/htacg/tidy-html5

.PHONY: tidy
tidy: apt-tidy
build: tidy

# tree
# -----------------------------------------------------------------------------

# http://mama.indstate.edu/users/ice/tree/

.PHONY: tree
tree: apt-tree
build: tree

# vale
# -----------------------------------------------------------------------------

# https://github.com/errata-ai/vale

VALE_BIN = vale
VALE_DIR = $(TMP_DIR)/$(VALE_BIN)
VALE_VERSION = 2.17.0
VALE_REPO = errata-ai/vale
VALE_TGZ = $(VALE_BIN)_$(VALE_VERSION)_Linux_64-bit.tar.gz
VALE_SIG = $(VALE_BIN)_$(VALE_VERSION)_checksums.txt
VALE_TGZ_URL = $(call gh_url,$(VALE_REPO),v$(VALE_VERSION),$(VALE_TGZ))
VALE_SIG_URL = $(call gh_url,$(VALE_REPO),v$(VALE_VERSION),$(VALE_SIG))

.PHONY: vale
vale: pip-docutils
	$(call gh_test_latest,$(VALE_REPO),v$(VALE_VERSION))
	$(call reset_dir,$(VALE_DIR))
	$(CURL) $(VALE_TGZ_URL) >$(VALE_DIR)/$(VALE_TGZ)
	$(CURL) $(VALE_SIG_URL) >$(VALE_DIR)/$(VALE_SIG)
	cd $(VALE_DIR) && sha256sum --check --ignore-missing $(VALE_SIG)
	cd $(VALE_DIR) && $(UNTGZ) $(VALE_TGZ)
	cd $(VALE_DIR) && $(call install_bin,$(VALE_BIN))
	rm -rf $(VALE_DIR)
build: vale

# vale-server
# -----------------------------------------------------------------------------

# https://github.com/errata-ai/vale-server

# VALE_SERVER_BIN = vale-server
# VALE_SERVER_DIR = $(VALE_SERVER_BIN)/$(TMP_DIR)
# VALE_SERVER_REPO = errata-ai/vale-server
# VALE_SERVER_VERSION = 2.0.0
# VALE_SERVER_APP = Vale-Server-$(VALE_SERVER_VERSION)-linux.AppImage
# VALE_SERVER_APP_URL = $(call gh_url, \
# 	$(VALE_SERVER_REPO),v$(VALE_SERVER_VERSION),$(VALE_SERVER_APP))
# VALE_SERVER_INSTALL = $(USER_LOCAL)/vale
# VALE_SERVER_INSTALL_BIN = $(VALE_SERVER_INSTALL)/usr/bin/$(VALE_SERVER_BIN)

# Vale Sever APT dependencies:
#
# - xserver-xorg-video-dummy
# - menu-xdg
# - dbus-x11
# - python3-pyinotify
# - xpra

# .PHONY: vale-server
# vale-server:
# 	$(call gh_test_latest,$(VALE_SERVER_REPO),v$(VALE_SERVER_VERSION))
# 	$(call reset_dir,$(VALE_SERVER_DIR))
# 	$(CURL) $(VALE_SERVER_APP_URL) >$(VALE_SERVER_DIR)/$(VALE_SERVER_APP)
# 	@ # Extract the AppImage to a directory so we can use without FUSE (which
# 	@ # is impractical inside a devcontainer)
# 	chmod 755 $(VALE_SERVER_DIR)/$(VALE_SERVER_APP)
# 	cd $(VALE_SERVER_DIR) && ./$(VALE_SERVER_APP) --appimage-extract >/dev/null
# 	@ # Install into the user's local directory because Vale Sever modifies its
# 	@ # own files when run (making it unsuitable for a root installation)
# 	mkdir -p $(USER_LOCAL)/bin
# 	rm -rf $(VALE_SERVER_INSTALL)
# 	mv $(VALE_SERVER_DIR)/squashfs-root $(VALE_SERVER_INSTALL)
# 	ln -sf $(VALE_SERVER_INSTALL_BIN) $(USER_LOCAL)/bin/$(VALE_SERVER_BIN)
# 	chown -R $(USER):$(USER) $(USER_LOCAL)
# 	rm -f $(VALE_SERVER_DIR)

# yamllint
# -----------------------------------------------------------------------------

# https://github.com/adrienverge/yamllint

.PHONY: yamllint
yamllint: apt-yamllint
build: yamllint

# yarn
# -----------------------------------------------------------------------------

# https://github.com/yarnpkg/yarn

.PHONY: yarn
yarn: npm-yarn
build: yarn

# Secondary prerequisites
# =============================================================================

$(TMP_DIR):
	@ mkdir -p $(TMP_DIR)

# $(call echo_run,rule)
define echo_run
echo $(1) && $(1)
endef

# apt
# -----------------------------------------------------------------------------

apt: $(TMP_DIR)
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,apt-get update $(APT_GET_OPTS)); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# apt-%
# -----------------------------------------------------------------------------

DEBIAN_FRONTEND = noninteractive
APT_GET_OPTS = -y --no-install-recommends
APT_GET_INSTALL = apt-get install $(APT_GET_OPTS)

apt-%: apt
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(APT_GET_INSTALL) $*); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# cargo.stamp
# -----------------------------------------------------------------------------

RUSTUP_URL = https://sh.rustup.rs
RUSTUP_FILE = $(TMP_DIR)/rustup.sh

cargo: apt-pkg-config
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(CURL) $(RUSTUP_URL) >$(RUSTUP_FILE)); \
		$(call echo_run,chmod 755 $(RUSTUP_FILE)); \
		$(call echo_run,$(RUSTUP_FILE) -y --no-modify-path); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# cargo-%
# -----------------------------------------------------------------------------

DEBIAN_FRONTEND = noninteractive
CARGO_INSTALL = cargo install $(APT_GET_OPTS)

cargo-%: cargo
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(CARGO_INSTALL) $*); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# nodejs
# -----------------------------------------------------------------------------

NODESOURCE_URL = https://deb.nodesource.com/setup_16.x
NODESOURCE_FILE = $(TMP_DIR)/nodesource_setup.sh
APT_GET_AUTOREMOVE = apt-get autoremove -y

nodejs:
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(CURL) $(NODESOURCE_URL) >$(NODESOURCE_FILE)); \
		$(call echo_run,chmod 755 $(NODESOURCE_FILE)); \
		$(call echo_run,$(NODESOURCE_FILE)); \
		$(call echo_run,$(APT_GET_INSTALL) $@); \
		$(call echo_run,$(APT_GET_AUTOREMOVE)); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# npm
# -----------------------------------------------------------------------------

npm: nodejs
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,npm config set fund false --global); \
		$(call echo_run,$(NPM_INSTALL) npm@latest); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# npm-%
# -----------------------------------------------------------------------------

NPM_OPTS = --global --no-audit --prefer-dedupe
NPM_INSTALL = npm install $(NPM_OPTS)

npm-%: npm
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(NPM_INSTALL) $*); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# pip
# -----------------------------------------------------------------------------

PIP_APT_DEPS = \
	apt-python3 \
	apt-python3-doc \
	apt-python3-pip \
	apt-python3-wheel \
	apt-python3-venv

pip: $(PIP_APT_DEPS)
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(PIP_INSTALL) pip); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# pip-%
# -----------------------------------------------------------------------------

PIP_INSTALL = pip install --no-cache-dir --upgrade

pip-%: pip
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(PIP_INSTALL) $*); \
		touch $(TMP_DIR)/$@.stamp; \
	fi

# pipx
# -----------------------------------------------------------------------------

pipx: pip-pipx

# pipx-%
# -----------------------------------------------------------------------------

PIPX_INSTALL = pipx install --force

pipx-%: pipx
	@ if ! test -f $(TMP_DIR)/$@.stamp; then \
		$(call echo_run,$(PIPX_INSTALL) $*); \
		touch $(TMP_DIR)/$@.stamp; \
	fi
