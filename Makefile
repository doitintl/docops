# =============================================================================
# Primary project build system
# =============================================================================

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL=C

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

.DEFAULT_GOAL: checks

.PHONY: checks
checks:

# dockerfilelint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/replicatedhq/dockerfilelint

# DOCKERFILELINT := dockerfilelint

# all: dockerfilelint
# .PHONY: dockerfilelint
# dockerfilelint:
# 	$(call print-target)
# 	find . -name 'Dockerfile' -print0 | xargs -0 $(DOCKERFILELINT)

# hadolint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/hadolint/hadolint

# HADOLINT := hadolint

# Disabled until `hadolint` is available in the published devcontainer

# checks: hadolint
# .PHONY: hadolint
# hadolint:
# 	$(call print-target)
# 	find . -name 'Dockerfile' -print0 | xargs -0 $(HADOLINT)
