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


.DEFAULT_GOAL = test

CMD            := docops-gloss-terms
CMP_DOCS       := examples/gitbook/cmp-docs
TEST_CONFIG    := data/configs/test

MAKEFILE       := $(lastword $(MAKEFILE_LIST))
RULES_DIR      := $(dir $(MAKEFILE))
RULES_FILE     := $(subst $(RULES_DIR),,$(MAKEFILE_LIST))
RULES          := $(basename $(RULES_FILE))
CMD_LOG_DIR    := $(LOG_DIR)/$(RULES)

COLOR_MAKEFILE :=\e[0;36m$(MAKEFILE)\e[0;00m
COLOR_TEST      =\e[0;35m$@\e[0;00m
PRINT_MAKE_CMD  = @ printf "make -f $(COLOR_MAKEFILE) $(COLOR_TEST)\n"
LOGFILE         = $(CMD_LOG_DIR)/$@.log

$(CMD_LOG_DIR):
	mkdir -p "$@"

.PHONY: test-cli-init
test-cli-init: $(CMD_LOG_DIR)

.PHONY: test-cli-no-args
test-cli-no-args: test-cli-init
	$(PRINT_MAKE_CMD)
	$(CMD) || true \
	    > $(LOGFILE)

.PHONY: test-cli-version
test-cli-version: test-cli-no-args
	$(PRINT_MAKE_CMD)
	$(CMD) --version \
	    > $(LOGFILE)

.PHONY: test-cli-help
test-cli-help: test-cli-version
	$(PRINT_MAKE_CMD)
	$(CMD) --help \
	    > $(LOGFILE)

.PHONY: test-cli-no-output
test-cli-table-type: test-cli-row-limit
	$(PRINT_MAKE_CMD)
	$(CMD) (CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-no-config
test-cli-no-config: test-cli-help
	$(PRINT_MAKE_CMD)
	$(CMD) -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-no-config-verbose
test-cli-no-config-verbose: test-cli-no-config
	$(PRINT_MAKE_CMD)
	$(CMD) -v -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-no-config-quiet
test-cli-no-config-quiet: test-cli-no-config-verbose
	$(PRINT_MAKE_CMD)
	$(CMD) -q -o table $(CMP_DOCS) \
	    > $(LOGFILE)

# TODO: This rule seems to pass if there's an error output
# Trick the program into thinking it's running in a TTY so that it will
# colorize output if configured to do so. Then, replace the start of any ANSI
# escape secquence with the UUID. If we can successfully `grep` for that UUID,
# then the `--disable-ansi` option failed.
.PHONY: test-cli-disable-ansi
test-cli-disable-ansi: test-cli-no-config-quiet
	$(PRINT_MAKE_CMD)
	@ # Generate UUID for ANSI test to avoid accidentally matching terms (e.g.,
	@ # when pointing the command at it's own source directory)
	uuid="$$(uuidgen)" && \
	if socat - EXEC:"$(CMD) --disable-ansi \
	        $(CMP_DOCS)",pty,setsid,ctty | \
	        perl -pe "s/\033.*/$${uuid}/g" | \
	        grep "$${uuid}"; then\
	    false; \
	fi > $(LOGFILE)

.PHONY: test-cli-config
test-cli-config: test-cli-disable-ansi
	$(PRINT_MAKE_CMD)
	$(CMD) -c $(TEST_CONFIG) -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-config-verbose
test-cli-config-verbose: test-cli-config
	$(PRINT_MAKE_CMD)
	$(CMD) -v -c $(TEST_CONFIG) -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-config-quiet
test-cli-config-quiet: test-cli-config-verbose
	$(PRINT_MAKE_CMD)
	$(CMD) -q -c $(TEST_CONFIG) -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-row-limit
test-cli-row-limit: test-cli-config-quiet
	$(PRINT_MAKE_CMD)
	$(CMD) -l 10 -o table $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-table-type
test-cli-table-type: test-cli-row-limit
	$(PRINT_MAKE_CMD)
	$(CMD) -o table -t github $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-show-output-types
test-cli-show-output-types: test-cli-table-type
	$(PRINT_MAKE_CMD)
	$(CMD) --show-output-types \
	    > $(LOGFILE)

.PHONY: test-cli-show-formats
test-cli-show-table-formats: test-cli-show-output-types
	$(PRINT_MAKE_CMD)
	$(CMD) --show-table-formats \
	    > $(LOGFILE)

.PHONY: test-cli-print-cache
test-cli-print-cache: test-cli-show-table-formats
	$(PRINT_MAKE_CMD)
	$(CMD) --print-cache \
        > $(LOGFILE)

.PHONY: test-cli-delete-cache
test-cli-delete-cache: test-cli-print-cache
	$(PRINT_MAKE_CMD)
	$(CMD) --delete-cache \
	    > $(LOGFILE)

.PHONY: test-cli-show-warnings
test-cli-show-warnings: test-cli-delete-cache
	$(PRINT_MAKE_CMD)
	$(CMD) --show-warnings $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test
test: test-cli-show-warnings
