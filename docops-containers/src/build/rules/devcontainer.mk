# =============================================================================
# Build a development container image
# =============================================================================

.POSIX:

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

RULES_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
INSTALL_RULES = $(RULES_DIR)/install.mk

INSTALL = $(MAKE) --no-print-directory -f $(INSTALL_RULES)

# Targets
# =============================================================================

# dev
# -----------------------------------------------------------------------------

DEV_DEPS = \
	bashrc \
	brok \
	build-essential \
	cspell \
	codespell \
	dockerfilelint \
	doitintl-docops \
	ec \
	fdupes \
	file \
	hadolint \
	html-minifier \
	imgdup2go \
	lintspaces-cli \
	markdown-link-check \
	markdownlint-cli \
	misspell \
	optipng \
	pandoc \
	parallel \
	prettier \
	proselint \
	shellcheck \
	shfmt \
	tidy \
	vale \
	yamllint

.PHONY: dev
dev:
	@ $(INSTALL) $(DEV_DEPS)

# dev-python
# -----------------------------------------------------------------------------

DEV_PYTHON_DEPS = poetry

.PHONY: dev-python
dev-python: dev
	@ $(INSTALL) $(DEV_PYTHON_DEPS)

# Default goal
# =============================================================================

# Clears the default goal, causing an error if no target is specified
.DEFAULT_GOAL =
