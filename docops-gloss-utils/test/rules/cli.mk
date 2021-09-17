.DEFAULT_GOAL = test

CMD         := dgloss-analyze-terms
CMP_DOCS    := examples/gitbook/cmp-docs
TEST_CONFIG := data/configs/test
CLI_LOG_DIR := $(LOG_DIR)/cli

PRINT_TEST = @ printf "Running test: \033[1m$(subst test-,,$@)\033[00m\n"
LOGFILE    = $(CLI_LOG_DIR)/$@.log

$(CLI_LOG_DIR):
	mkdir -p "$@"

.PHONY: test-cli-init
test-cli-init: $(CLI_LOG_DIR)

.PHONY: test-cli-no-args
test-cli-no-args: test-cli-init
	$(PRINT_TEST)
	$(CMD) || true \
	    > $(LOGFILE)

.PHONY: test-cli-version
test-cli-version: test-cli-no-args
	$(PRINT_TEST)
	$(CMD) --version \
	    > $(LOGFILE)

.PHONY: test-cli-help
test-cli-help: test-cli-version
	$(PRINT_TEST)
	$(CMD) --help \
	    > $(LOGFILE)

.PHONY: test-cli-no-config
test-cli-no-config: test-cli-help
	$(PRINT_TEST)
	$(CMD) $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-no-config-verbose
test-cli-no-config-verbose: test-cli-no-config
	$(PRINT_TEST)
	$(CMD) -v $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-no-config-quiet
test-cli-no-config-quiet: test-cli-no-config-verbose
	$(PRINT_TEST)
	$(CMD) -q $(CMP_DOCS) \
	    > $(LOGFILE)

# Trick the program into thinking it's running in a TTY so that it will
# colorize output if configured to do so. Then, replace the start of any ANSI
# escape secquence with the UUID. If we can successfully `grep` for that UUID,
# then the `--disable-ansi` option failed.
.PHONY: test-cli-disable-ansi
test-cli-disable-ansi: test-cli-no-config-quiet
	$(PRINT_TEST)
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
	$(PRINT_TEST)
	$(CMD) -c $(TEST_CONFIG) $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-config-verbose
test-cli-config-verbose: test-cli-config
	$(PRINT_TEST)
	$(CMD) -v -c $(TEST_CONFIG) $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-config-quiet
test-cli-config-quiet: test-cli-config-verbose
	$(PRINT_TEST)
	$(CMD) -q -c $(TEST_CONFIG) $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-row-limit
test-cli-row-limit: test-cli-config-quiet
	$(PRINT_TEST)
	$(CMD) -l 10 $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-table-type
test-cli-table-type: test-cli-row-limit
	$(PRINT_TEST)
	$(CMD) -t github $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test-cli-show-formats
test-cli-show-formats: test-cli-table-type
	$(PRINT_TEST)
	$(CMD) --show-formats \
	    > $(LOGFILE)

.PHONY: test-cli-print-cache
test-cli-print-cache: test-cli-show-formats
	$(PRINT_TEST)
	$(CMD) --print-cache \
        > $(LOGFILE)

.PHONY: test-cli-delete-cache
test-cli-delete-cache: test-cli-print-cache
	$(PRINT_TEST)
	$(CMD) --delete-cache \
	    > $(LOGFILE)

.PHONY: test-cli-show-warnings
test-cli-show-warnings: test-cli-delete-cache
	$(PRINT_TEST)
	$(CMD) --show-warnings $(CMP_DOCS) \
	    > $(LOGFILE)

.PHONY: test
test: test-cli-show-warnings
