#!/bin/sh -e

# Test the `zapier.py` by posting the result to a Slack webhook (defined by the
# `SLACK_APP_RTD_WEBOOK_TEST` environment variable)

python3 zapier.py |
    curl -H 'Content-type: application/json' \
        -X POST --data-binary @- "${SLACK_APP_RTD_WEBOOK_TEST}"

# The HTTP response body lacks a final newline so we add one manually
printf '\n'
