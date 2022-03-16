# =============================================================================
# Prepare the container image
# =============================================================================

# This Makefile is copied into the container image by the Dockerfile

.POSIX:

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

SRC_DIR := $(subst /,,$(dir $(lastword $(MAKEFILE_LIST))))
PREP_DIR := $(SRC_DIR)/prep
TMP_DIR := $(PREP_DIR)/tmp
PREP_RULES := $(PREP_DIR)/rules.mk

MAKE_PREP := $(MAKE) --no-print-directory -f $(PREP_RULES)

PREP_DEPS = \
	dotfiles \
	black \
	brok \
	build-essential \
	codespell \
	cspell \
	dockerfilelint \
	doitintl-docops \
	ec \
	fd-find \
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
	textlint \
	tidy \
	tree \
	vale \
	yamllint \
	yarn

# Targets
# =============================================================================

.DEFAULT_GOAL := prep

.PHONY: list
list:
	@$(PREP_DIR)/list.sh

.PHONY: list
list-check:
	@$(PREP_DIR)/list.sh --check

.PHONY: prep
prep: $(PREP_DEPS)

.PHONY: clean
clean:
	rm -rf $(TMP_DIR)

# Pattern rules
# =============================================================================

%:
	@ $(MAKE_PREP) $@
