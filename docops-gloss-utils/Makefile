.EXPORT_ALL_VARIABLES:

.DEFAULT_GOAL = help

VENV       := $(shell poetry env info --path)
PATH       := $(VENV)/bin:$(PATH)
INIT_STAMP := init.stamp
LOG_DIR    := test/logs
TEST_DIR   := test/rules

MAKE_TESTS = $(MAKE) -C . -f

.DEFAULT_GOAL := help
.PHONY: help # Print this help message and exit
help:
	@ echo "Usage:"
	@ echo
	@ @grep -E '^.PHONY:' $(MAKEFILE_LIST) | \
	    grep "#" | sed 's,.*: ,,' | \
		awk 'BEGIN {FS = " # "}; {printf "  make %s,%s\n", $$1, $$2}' | \
		column -t -s ','

$(INIT_STAMP):
	git submodule update --init --recursive
	poetry update
	poetry install
	@ touch $@

.PHONY: init # Initialize the development environment
init: $(INIT_STAMP)

.PHONY: reset # Reset the development environment
reset:
	rm -rf "$(VENV)"
	rm -rf "$(INIT_STAMP)"

.PHONY: test # Run project tests
test: init
	rm -rf "$(LOG_DIR)"
	poetry run $(MAKE_TESTS) $(TEST_DIR)/cli.mk
