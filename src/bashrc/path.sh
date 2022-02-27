# shellcheck shell=bash
# shellcheck disable=SC1090
# shellcheck disable=SC1091

# Source `.profile` (for `PATH` additions) without causing an infinite loop
# https://github.com/koalaman/shellcheck/wiki/SC1091
BASH_VERSION="" . "${HOME}/.profile"
