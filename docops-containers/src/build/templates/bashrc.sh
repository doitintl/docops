# shellcheck shell=bash
# shellcheck disable=SC1090
# shellcheck disable=SC1091

# Fix the awful default VS Code directory colors
eval "$(dircolors -p |
    sed 's/ 4[0-9];/ 01;/; s/;4[0-9];/;01;/g; s/;4[0-9] /;01 /' |
    dircolors /dev/stdin)" || true

# Configure Git
git config --global 'pull.rebase' 'true'
git config --global 'push.default' 'current'
git config --global 'branch.autosetuprebase' 'always'

# Source `.profile` (for `PATH` additions) without causing an infinite loop
# https://github.com/koalaman/shellcheck/wiki/SC1091
BASH_VERSION="" . "${HOME}/.profile"

# Initialize shell completion
. /usr/share/bash-completion/bash_completion
