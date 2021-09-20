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

CMD            := poetry

# TODO: DRY OUT THIS BOILERPLATE TEXT
MAKEFILE       := $(lastword $(MAKEFILE_LIST))
RULES_DIR      := $(dir $(MAKEFILE))
RULES_FILE     := $(subst $(RULES_DIR),,$(MAKEFILE_LIST))
RULES          := $(basename $(RULES_FILE))
CMD_LOG_DIR    := $(LOG_DIR)/$(RULES_DIR)/$(RULES)

COLOR_MAKEFILE :=\e[0;36m$(MAKEFILE)\e[0;00m
COLOR_TEST      =\e[0;35m$@\e[0;00m
PRINT_MAKE_CMD  = @ printf "make -f $(COLOR_MAKEFILE) $(COLOR_TEST)\n"
LOGFILE         = $(CMD_LOG_DIR)/$@.log

$(CMD_LOG_DIR):
	mkdir -p "$@"

PHONY: test-cli-poetry-check
test-cli-poetry-check: $(CMD_LOG_DIR)
	$(PRINT_MAKE_CMD)
	$(CMD) check --no-ansi \
	    > $(LOGFILE)

.PHONY: test-cli-poetry-build
test-cli-poetry-build: test-cli-poetry-check
	$(PRINT_MAKE_CMD)
	$(CMD) build --no-ansi \
	    > $(LOGFILE)

# .PHONY: test-cli-poetry-publish-dry-run
# test-cli-poetry-publish-dry-run: test-cli-poetry-build
# 	#(PRINT_MAKE_CMD)
# 	$(CMD) publish --dry-run --no-ansi \
# 	    > $(LOGFILE)

.PHONY: test
test: test-cli-poetry-build
