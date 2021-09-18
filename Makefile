# MIT License

# Copyright 2021, DoiT International

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


.EXPORT_ALL_VARIABLES:

.DEFAULT_GOAL = help

VENV       := $(shell poetry env info --path)
PATH       := $(VENV)/bin:$(PATH)
INIT_STAMP := init.stamp
LOG_DIR    := tests/logs
TEST_DIR   := tests/rules

MAKE_TESTS = $(MAKE) -C . -f

.PHONY: help # Print this help message and exit
help:
	@ echo "Usage:"
	@ echo
	@ @grep -E '^.PHONY:' $(MAKEFILE_LIST) | \
	    grep "#" | sed 's,.*: ,,' | \
	    awk 'BEGIN {FS = " # "}; {printf "  make %s,%s\n", $$1, $$2}' | \
	    column -t -s ','

$(INIT_STAMP):
	mkdir -p examples/gitbook/cmp-docs
	git submodule update --init --recursive
	poetry update
	@ echo
	poetry install
	@ touch $@
	@ echo
	@ printf "\e[0;34mRun \`\e[4;34mpoetry shell\e[0;34m\` to activate your "
	@ printf "Python virtual environment\e[0;00m\n"
	@ echo

.PHONY: init # Initialize the development environment
init: $(INIT_STAMP)

.PHONY: update # Update the development environment
update:
	$(MAKE) reset
	$(MAKE) init


.PHONY: reset # Reset the development environment
reset:
	rm -rf "$(VENV)"
	rm -rf "$(INIT_STAMP)"

.PHONY: test # Run project tests
test: init
	rm -rf "$(LOG_DIR)"
	poetry run $(MAKE_TESTS) $(TEST_DIR)/docops-gitbook.mk
	poetry run $(MAKE_TESTS) $(TEST_DIR)/docops-gloss-terms.mk
