# =============================================================================
# Primary project build system
# =============================================================================

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL=C

# ANSI formatting
BOLD = [1m
RESET = [0m

# Functions
# =============================================================================

# $(call print-target)
define print-target
@ printf "\e$(BOLD)make %s\e$(RESET)\n" "$$(echo $@ | sed 's,.stamp,,')"
endef

# Targets
# =============================================================================

# checks
# -----------------------------------------------------------------------------

.DEFAULT_GOAL: check

.PHONY: check
check:

# dockerfilelint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/replicatedhq/dockerfilelint

DOCKERFILELINT := dockerfilelint

check: dockerfilelint
.PHONY: dockerfilelint
dockerfilelint:
	$(call print-target)
	find . -name 'Dockerfile' -print0 | xargs -0 $(DOCKERFILELINT)

# hadolint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/hadolint/hadolint

HADOLINT := hadolint

check: hadolint
.PHONY: hadolint
hadolint:
	$(call print-target)
	find . -name 'Dockerfile' -print0 | xargs -0 $(HADOLINT)

# yamllint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/adrienverge/yamllint

YAMLLINT := yamllint .

check: yamllint
.PHONY: yamllint
yamllint:
	$(call print-target)
	$(YAMLLINT)

# black
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/psf/black

BLACK := black --check .

check: black
.PHONY: black
black:
	$(call print-target)
	$(BLACK)
