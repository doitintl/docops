# =============================================================================
# Build a development container image
# =============================================================================

.POSIX:

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

SRC_DIR := $(subst /,,$(dir $(lastword $(MAKEFILE_LIST))))
BUILD_DIR := $(SRC_DIR)/build
TMP_DIR := $(BUILD_DIR)/tmp
RULES := $(BUILD_DIR)/rules.mk

MAKE_RULES := $(MAKE) --no-print-directory -f $(RULES)

BUILD_DEPS = \
	bashrc \
	brok \
	build-essential \
	codespell \
	cspell \
	dockerfilelint \
	doitintl-docops \
	ec \
	fdupes \
	file \
	hadolint \
	html-minifier \
	imagemagick \
	imgdup2go \
	lintspaces-cli \
	markdown-link-check \
	markdownlint-cli \
	misspell \
	optipng \
	pandoc \
	parallel \
	poetry \
	prettier \
	proselint \
	shellcheck \
	shfmt \
	tidy \
	vale \
	yamllint

# Targets
# =============================================================================

.DEFAULT_GOAL := build

.PHONY: list
list:
	@$(BUILD_DIR)/list.sh

.PHONY: list
list-check:
	@$(BUILD_DIR)/list.sh --check

.PHONY: build
build: $(BUILD_DEPS)

.PHONY: clean
clean:
	rm -rf $(TMP_DIR)

# Pattern rules
# =============================================================================

%:
	@ $(MAKE_RULES) $@
