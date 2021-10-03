#!/bin/sh -e

# Package managers
# -----------------------------------------------------------------------------

GITHUB_BASE="https://raw.githubusercontent.com"
INSTALL_BREW="${GITHUB_BASE}/Homebrew/install/HEAD/install.sh"

cd "${HOME}"
curl -fsSL "${INSTALL_BREW}" > /tmp/install-homebrew.sh
chmod 755 /tmp/install-homebrew.sh
/tmp/install-homebrew.sh

eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

brew doctor

brew install node
npm install -g npm

# Basic tools
# -----------------------------------------------------------------------------

brew install gh act

npm install -g editorconfig
npm install -g prettier

brew install hadolint
npm install -g dockerfilelint

npm install -g shellcheck
brew install checkbashisms

brew install markdownlint-cli
npm install -g markdown-link-check

npm install -g cspell
brew install get-woke/tap/woke

# Python
# -----------------------------------------------------------------------------

brew install pyenv

# Bash
# -----------------------------------------------------------------------------

cat /tmp/build/config/bash.sh >> "/home/vscode/.bashrc"

# Clean up
# -----------------------------------------------------------------------------

npm dedupe
npm prune

brew cleanup -s
