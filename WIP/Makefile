LOCAL_DIR = $(dir $(lastword $(MAKEFILE_LIST)))
VENV_DIR  = $(abspath $(LOCAL_DIR)/.venv)

AB := $(shell tput bold) # ANSI bold text
AR := $(shell tput sgr0) # ANSI reset

.PHONY: help
help:
	@ printf 'Run `make <TARGET>`, where <TARGET> is one of:\n'
	@ echo
	@ printf '  $(AB)install$(AR)  Install the Python package dependencies\n'
	@ echo
	@ printf '  $(AB)build$(AR)    Build the Python package\n'
	@ echo
	@ printf '  $(AB)publish$(AR)  Publish the Python package to PyPI\n'
	@ echo
	@ printf '  $(AB)reset$(AR)    Reset the Python virtual environment\n'


.PHONY: install
install:
	cd "${LOCAL_DIR}" && poetry install

.PHONY: build
build:
	cd "${LOCAL_DIR}" && poetry build

.PHONY: publish
publish: build
	cd "${LOCAL_DIR}" && poetry publish

.PHONY: reset
reset:
	rm -rf "$(VENV_DIR)"