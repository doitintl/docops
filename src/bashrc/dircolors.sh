# shellcheck shell=bash

# Fix the awful default VS Code directory colors
eval "$(dircolors -p |
    sed 's/ 4[0-9];/ 01;/; s/;4[0-9];/;01;/g; s/;4[0-9] /;01 /' |
    dircolors /dev/stdin)"
