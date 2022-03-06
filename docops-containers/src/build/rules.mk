# =============================================================================
# Install and configure software packages
# =============================================================================

.POSIX:

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

# ANSI formatting
BOLD = [1m
RED = [31m
RESET = [0m

BUILD_DIR := $(subst /,,$(dir $(lastword $(MAKEFILE_LIST))))
TEMPLATES_DIR := $(BUILD_DIR)/templates
TMP_DIR := $(BUILD_DIR)/tmp

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

# Functions
# =============================================================================

# print_target
# -----------------------------------------------------------------------------

# If `target` is empty, `$@` is used

# $(call print_target,target)
define print_target
@ printf "\e$(BOLD)make %s\e$(RESET)\n" "$$(echo $(firstword $(1) $@))"
endef

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
	printf '\e$(RED)Version mismatch\e$(RESET)\n'; \
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

# Targets
# =============================================================================

# dotfiles
# -----------------------------------------------------------------------------

BASHRC_SRC = $(TEMPLATES_DIR)/bashrc.sh

BASHRC_DEST = .bash_docops
FIRST_RUN = .config/vscode-dev-containers/first-run-notice-already-displayed
WILL_CITE = .parallel/will-cite

# $(call touch_file,user,file)
define touch_file
mkdir -p $(dir $(2))
touch $(2)
chown -R $(1):$(1) $(dir $(2))
endef

# $(call install_bashrc,user,home)
define install_bashrc
cp $(BASHRC_SRC) $(2)/$(BASHRC_DEST)
chown $(1):$(1) $(2)/$(BASHRC_DEST)
sed -i '/^.*$(BASHRC_DEST)$$/d' $(2)/.bashrc
printf '\n. ~/$(BASHRC_DEST)\n' >>$(2)/.bashrc
gawk -i inplace 'NF{c=1} (c++)<3' $(2)/.bashrc
endef

# TODO: Testing this rule results in many copies of the same changes made to
# your actual `.bashrc` file. We should remove any existing modifications
# before applying changes.
.PHONY: bashrc
bashrc: apt-bash-completion apt-gawk
	$(call print_target)
	$(call install_bashrc,$(ROOT),$(ROOT_HOME))
	$(call touch_file,$(ROOT),$(ROOT_HOME)/$(WILL_CITE))
	$(call install_bashrc,$(USER),$(USER_HOME))
	$(call touch_file,$(USER),$(USER_HOME)/$(WILL_CITE))
	$(call touch_file,$(USER),$(USER_HOME)/$(FIRST_RUN))

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
	$(call print_target)
	$(call gh_test_latest,$(BROK_REPO),$(BROK_VERSION))
	$(call reset_dir,$(BROK_DIR))
	$(CURL) $(BROK_DEB_URL) >$(BROK_DIR)/$(BROK_DEB)
	dpkg -i $(BROK_DIR)/$(BROK_DEB)
	rm -rf $(BROK_DIR)

# build-essential
# -----------------------------------------------------------------------------

# build-essential
# https://packages.debian.org/bullseye/build-essential

.PHONY: build-essential
build-essential: apt-build-essential

# codespell
# -----------------------------------------------------------------------------

# codespell
# https://github.com/codespell-project/codespell

.PHONY: codespell
codespell: pipx-codespell

# cspell
# -----------------------------------------------------------------------------

# cspell
# https://github.com/streetsidesoftware/cspell

.PHONY: cspell
cspell: npm-cspell

# dockerfilelint
# -----------------------------------------------------------------------------

# https://github.com/replicatedhq/dockerfilelint

.PHONY: dockerfilelint
dockerfilelint: npm-dockerfilelint

# doitintl-docops
# -----------------------------------------------------------------------------

# https://github.com/doitintl/docops-cli

.PHONY: doitintl-docops
doitintl-docops: pipx-doitintl-docops

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
	$(call print_target)
	$(call gh_test_latest,$(EC_REPO),$(EC_VERSION))
	$(call reset_dir,$(EC_DIR))
	$(CURL) $(EC_URL) >$(EC_DIR)/$(EC_TGZ)
	cd $(EC_DIR) && $(UNTGZ) $(EC_TGZ)
	cd $(EC_DIR) && mv bin/$(EC_FILE) $(EC_BIN)
	cd $(EC_DIR) && $(call install_bin,$(EC_BIN))
	rm -rf $(EC_DIR)

# fdupes
# -----------------------------------------------------------------------------

# https://github.com/adrianlopezroche/fdupes

.PHONY: fdupes
fdupes: apt-fdupes

# file
# -----------------------------------------------------------------------------

# https://github.com/file/file

.PHONY: file
file: apt-file

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
HADOLINT_VERSION = 2.8.0
HADOLINT_REPO = hadolint/hadolint
HADOLINT_FILE = $(HADOLINT_BIN)-Linux-x86_64
HADOLINT_FILE_URL = $(call gh_url, \
	$(HADOLINT_REPO),v$(HADOLINT_VERSION),$(HADOLINT_FILE))

# TODO: Create temporary directory

.PHONY: hadolint
hadolint:
	$(call print_target)
	$(call gh_test_latest,$(HADOLINT_REPO),v$(HADOLINT_VERSION))
	$(call reset_dir,$(HADOLINT_DIR))
	$(CURL) $(HADOLINT_FILE_URL) >$(HADOLINT_DIR)/$(HADOLINT_BIN)
	$(call install_bin,$(HADOLINT_DIR)/$(HADOLINT_BIN))
	rm -rf $(HADOLINT_DIR)

# html-minifier
# -----------------------------------------------------------------------------

# https://github.com/kangax/html-minifier

.PHONY: html-minifier
html-minifier: npm-html-minifier

# imagemagick
# -----------------------------------------------------------------------------

# https://github.com/ImageMagick/ImageMagick

.PHONY: imagemagick
imagemagick: apt-imagemagick

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

# TODO: Create temporary directory

.PHONY: imgdup2go
imgdup2go:
	$(call print_target)
	$(call gh_test_latest,$(IMGDUP2GO_REPO),v$(IMGDUP2GO_VERSION))
	$(call reset_dir,$(IMGDUP2GO_DIR))
	$(CURL) $(IMGDUP2GO_TGZ_URL) >$(IMGDUP2GO_DIR)/$(IMGDUP2GO_TGZ)
	cd $(IMGDUP2GO_DIR) && $(UNTGZ) $(IMGDUP2GO_TGZ)
	cd $(IMGDUP2GO_DIR) && $(call install_bin,$(IMGDUP2GO_BIN))
	rm -rf $(IMGDUP2GO_DIR)

# lintspaces-cli
# -----------------------------------------------------------------------------

# https://github.com/evanshortiss/lintspaces-cli

.PHONY: lintspaces-cli
lintspaces-cli: npm-lintspaces-cli

# markdown-link-check
# -----------------------------------------------------------------------------

# https://github.com/tcort/markdown-link-check

.PHONY: markdown-link-check
markdown-link-check: npm-markdown-link-check

# markdownlint-cli
# -----------------------------------------------------------------------------

# https://github.com/igorshubovych/markdownlint-cli

.PHONY: markdownlint-cli
markdownlint-cli: npm-markdownlint-cli

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

# TODO: Create temporary directory

.PHONY: misspell
misspell:
	$(call print_target)
	$(call gh_test_latest,$(MISSPELL_REPO),v$(MISSPELL_VERSION))
	$(call reset_dir,$(MISSPELL_DIR))
	$(CURL) $(MISSPELL_TGZ_URL) >$(MISSPELL_DIR)/$(MISSPELL_TGZ)
	cd $(MISSPELL_DIR) && $(UNTGZ) $(MISSPELL_TGZ)
	cd $(MISSPELL_DIR) && $(call install_bin,$(MISSPELL_BIN))
	rm -rf $(MISSPELL_DIR)

# optipng
# -----------------------------------------------------------------------------

# https://github.com/johnpaulada/optipng

.PHONY: optipng
optipng: apt-optipng

# pandoc
# -----------------------------------------------------------------------------

# https://github.com/jgm/pandoc

.PHONY: pandoc
pandoc: apt-pandoc

# parallel
# -----------------------------------------------------------------------------

# https://github.com/martinda/gnu-parallel

.PHONY: parallel
parallel: apt-parallel

# poetry
# -----------------------------------------------------------------------------

# https://github.com/python-poetry/poetry

.PHONY: poetry
poetry: pipx-poetry

# prettier
# -----------------------------------------------------------------------------

# https://github.com/prettier/prettier

.PHONY: prettier
prettier: npm-prettier

# proselint
# -----------------------------------------------------------------------------

# https://github.com/amperser/proselint

.PHONY: proselint
proselint: npm-proselint

# shellcheck
# -----------------------------------------------------------------------------

# https://github.com/koalaman/shellcheck

.PHONY: shellcheck
shellcheck: apt-shellcheck

# shfmt
# -----------------------------------------------------------------------------

# https://github.com/mvdan/sh#shfmt

SHFMT_BIN = shfmt
SHFMT_DIR = $(TMP_DIR)/$(SHFMT_BIN)
SHFMT_VERSION = 3.4.3
SHFMT_REPO = mvdan/sh
SHFMT_FILE = $(SHFMT_BIN)_v$(SHFMT_VERSION)_linux_amd64
SHFMT_FILE_URL = $(call gh_url, \
	$(SHFMT_REPO),v$(SHFMT_VERSION),$(SHFMT_FILE))

# TODO: Create temporary directory

.PHONY: shfmt
shfmt:
	$(call print_target)
	$(call gh_test_latest,$(SHFMT_REPO),v$(SHFMT_VERSION))
	$(call reset_dir,$(SHFMT_DIR))
	$(CURL) $(SHFMT_FILE_URL) >$(SHFMT_DIR)/$(SHFMT_BIN)
	$(call install_bin,$(SHFMT_DIR)/$(SHFMT_BIN))
	rm -rf $(SHFMT_DIR)

# textlint
# -----------------------------------------------------------------------------

# https://github.com/textlint/textlint

# TODO: Experiment with npm textlint packages:
#
# - textlint
# - @textlint-rule/textlint-rule-no-duplicate-abbr
# - @textlint-rule/textlint-rule-no-invalid-control-character
# - @textlint-rule/textlint-rule-no-unmatched-pair
# - textlint-filter-rule-allowlist
# - textlint-filter-rule-comments
# - textlint-filter-rule-node-types
# - textlint-rule-abbr-within-parentheses
# - textlint-rule-alex
# - textlint-rule-apostrophe
# - textlint-rule-commonmisspellings
# - textlint-rule-diacritics
# - textlint-rule-doubled-spaces
# - textlint-rule-en-capitalization
# - textlint-rule-en-max-word-count
# - textlint-rule-en-spell
# - textlint-rule-max-comma
# - textlint-rule-no-dead-link
# - textlint-rule-no-empty-section
# - textlint-rule-no-start-duplicated-conjunction
# - textlint-rule-no-todo
# - textlint-rule-no-zero-width-spaces
# - textlint-rule-rousseau
# - textlint-rule-spelling
# - textlint-rule-stop-words
# - textlint-rule-terminology
# - textlint-rule-unexpanded-acronym dictionary-en
# - textlint-rule-write-good

# tidy
# -----------------------------------------------------------------------------

# https://github.com/htacg/tidy-html5

.PHONY: tidy
tidy: apt-tidy

# vale
# -----------------------------------------------------------------------------

# https://github.com/errata-ai/vale

VALE_BIN = vale
VALE_DIR = $(TMP_DIR)/$(VALE_BIN)
VALE_VERSION = 2.15.2
VALE_REPO = errata-ai/vale
VALE_TGZ = $(VALE_BIN)_$(VALE_VERSION)_Linux_64-bit.tar.gz
VALE_SIG = $(VALE_BIN)_$(VALE_VERSION)_checksums.txt
VALE_TGZ_URL = $(call gh_url,$(VALE_REPO),v$(VALE_VERSION),$(VALE_TGZ))
VALE_SIG_URL = $(call gh_url,$(VALE_REPO),v$(VALE_VERSION),$(VALE_SIG))

# TODO: Create temporary directory

.PHONY: vale
vale:
	$(call print_target)
	$(call gh_test_latest,$(VALE_REPO),v$(VALE_VERSION))
	$(call reset_dir,$(VALE_DIR))
	$(CURL) $(VALE_TGZ_URL) >$(VALE_DIR)/$(VALE_TGZ)
	$(CURL) $(VALE_SIG_URL) >$(VALE_DIR)/$(VALE_SIG)
	cd $(VALE_DIR) && sha256sum --check --ignore-missing $(VALE_SIG)
	cd $(VALE_DIR) && $(UNTGZ) $(VALE_TGZ)
	cd $(VALE_DIR) && $(call install_bin,$(VALE_BIN))
	rm -rf $(VALE_DIR)

# vale-server
# -----------------------------------------------------------------------------

# https://github.com/errata-ai/vale-server

VALE_SERVER_BIN = vale-server
VALE_SERVER_DIR = $(VALE_SERVER_BIN)/$(TMP_DIR)
VALE_SERVER_REPO = errata-ai/vale-server
VALE_SERVER_VERSION = 2.0.0
VALE_SERVER_APP = Vale-Server-$(VALE_SERVER_VERSION)-linux.AppImage
VALE_SERVER_APP_URL = $(call gh_url, \
	$(VALE_SERVER_REPO),v$(VALE_SERVER_VERSION),$(VALE_SERVER_APP))
VALE_SERVER_INSTALL = $(USER_LOCAL)/vale
VALE_SERVER_INSTALL_BIN = $(VALE_SERVER_INSTALL)/usr/bin/$(VALE_SERVER_BIN)

# Vale Sever APT dependencies:
#
# - xserver-xorg-video-dummy
# - menu-xdg
# - dbus-x11
# - python3-pyinotify
# - xpra

# TODO: Create temporary directory

.PHONY: vale-server
vale-server:
	$(call print_target)
	$(call gh_test_latest,$(VALE_SERVER_REPO),v$(VALE_SERVER_VERSION))
	$(call reset_dir,$(VALE_SERVER_DIR))
	$(CURL) $(VALE_SERVER_APP_URL) >$(VALE_SERVER_DIR)/$(VALE_SERVER_APP)
	@ # Extract the AppImage to a directory so we can use without FUSE (which
	@ # is impractical inside a devcontainer)
	chmod 755 $(VALE_SERVER_DIR)/$(VALE_SERVER_APP)
	cd $(VALE_SERVER_DIR) && ./$(VALE_SERVER_APP) --appimage-extract >/dev/null
	@ # Install into the user's local directory because Vale Sever modifies its
	@ # own files when run (making it unsuitable for a root installation)
	mkdir -p $(USER_LOCAL)/bin
	rm -rf $(VALE_SERVER_INSTALL)
	mv $(VALE_SERVER_DIR)/squashfs-root $(VALE_SERVER_INSTALL)
	ln -sf $(VALE_SERVER_INSTALL_BIN) $(USER_LOCAL)/bin/$(VALE_SERVER_BIN)
	chown -R $(USER):$(USER) $(USER_LOCAL)
	rm -f $(VALE_SERVER_DIR)

# yamllint
# -----------------------------------------------------------------------------

# https://github.com/adrienverge/yamllint

.PHONY: yamllint
yamllint: apt-yamllint

# Pattern rules
# =============================================================================

# apt-%
# -----------------------------------------------------------------------------

DEBIAN_FRONTEND = noninteractive
APT_GET_OPTS = -y --no-install-recommends
APT_GET_INSTALL = apt-get install $(APT_GET_OPTS)

apt-%: $(TMP_DIR)/apt.stamp
	$(call print_target, $*)
	$(APT_GET_INSTALL) $*

# cargo-%
# -----------------------------------------------------------------------------

DEBIAN_FRONTEND = noninteractive
APT_GET_OPTS = -y --no-install-recommends
CARGO_INSTALL = cargo install $(APT_GET_OPTS)

acargopt-%: $(TMP_DIR)/cargo.stamp
	$(call print_target, $*)
	$(CARGO_INSTALL) $*

# npm-%
# -----------------------------------------------------------------------------

NPM_OPTS = --global --no-audit --prefer-dedupe
NPM_INSTALL = npm install $(NPM_OPTS)

npm-%: $(TMP_DIR)/npm.stamp
	$(call print_target, $*)
	$(NPM_INSTALL) $*

# pip-%
# -----------------------------------------------------------------------------

PIP_INSTALL = pip install --no-cache-dir --upgrade

pip-%: $(TMP_DIR)/pip.stamp
	$(call print_target, $*)
	$(PIP_INSTALL) $*

# pipx-%
# -----------------------------------------------------------------------------

PIPX_INSTALL = pipx install --force

pipx-%: $(TMP_DIR)/pipx.stamp
	$(call print_target, $*)
	$(PIPX_INSTALL) $*

# Stamp rules
# =============================================================================

# apt.stamp
# -----------------------------------------------------------------------------

$(TMP_DIR)/apt.stamp:
	apt-get update $(APT_GET_OPTS)
	mkdir -p $(TMP_DIR)
	touch $@

# cargo.stamp
# -----------------------------------------------------------------------------

# Currently unused (see `fixred` target)

# RUSTUP_URL = https://sh.rustup.rs

# $(TMP_DIR)/cargo.stamp: apt-pkg-config
# 	$(CURL) $(RUSTUP_URL) >$(TMP_DIR)/rustup.sh
# 	chmod 755 $(TMP_DIR)/rustup.sh
# 	$(TMP_DIR)/rustup.sh -y --no-modify-path
# 	mkdir -p $(TMP_DIR)
# 	touch $@

# npm.stamp
# -----------------------------------------------------------------------------

$(TMP_DIR)/npm.stamp: apt-npm
	npm config set fund false --global
	$(NPM_INSTALL) npm@latest
	mkdir -p $(TMP_DIR)
	touch $@

# pip.stamp
# -----------------------------------------------------------------------------

PIP_APT_DEPS = \
	apt-python3 \
	apt-python3-doc \
	apt-python3-pip \
	apt-python3-wheel \
	apt-python3-venv

$(TMP_DIR)/pip.stamp: $(PIP_APT_DEPS)
	$(PIP_INSTALL) pip
	mkdir -p $(TMP_DIR)
	touch $@

# pipx.stamp
# -----------------------------------------------------------------------------

$(TMP_DIR)/pipx.stamp: pip-pipx
	mkdir -p $(TMP_DIR)
	touch $@

# Default goal
# =============================================================================

# Clears the default goal, causing an error if no target is specified
.DEFAULT_GOAL =
