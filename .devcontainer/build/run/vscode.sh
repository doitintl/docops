#!/bin/sh -e

HOME="/home/vscode"

# Shell
# -----------------------------------------------------------------------------

BASHRC_DIRCOLORS="/tmp/build/dotfiles/bashrc/dircolors.sh"
BASHRC_PATH="/tmp/build/dotfiles/bashrc/path.sh"
PROFILE_BREW="/tmp/build/dotfiles/profile/brew.sh"
PROFILE_PYTHON="/tmp/build/dotfiles/profile/python.sh"

(echo && cat "${BASHRC_DIRCOLORS}") >>"${HOME}/.bashrc"
(echo && cat "${BASHRC_PATH}") >>"${HOME}/.bashrc"

# VS Code
# -----------------------------------------------------------------------------

VSCODE_CONFIG="${HOME}/.config/vscode-dev-containers"

# Disable first run notice message
mkdir -p "${VSCODE_CONFIG}"
touch "${VSCODE_CONFIG}first-run-notice-already-displayed"

# Homebrew
# -----------------------------------------------------------------------------

GITHUB_BASE="https://raw.githubusercontent.com"
INSTALL_BREW="${GITHUB_BASE}/Homebrew/install/HEAD/install.sh"

cd "${HOME}"
curl -fsSL "${INSTALL_BREW}" >/tmp/install-homebrew.sh
chmod 755 /tmp/install-homebrew.sh
/tmp/install-homebrew.sh

(echo && cat "${PROFILE_BREW}") >>"${HOME}/.profile"
# https://github.com/koalaman/shellcheck/wiki/SC1090
# shellcheck disable=SC1090
. "${PROFILE_BREW}"

brew doctor

# Python
# -----------------------------------------------------------------------------

(echo && cat "${PROFILE_PYTHON}") >>"${HOME}/.profile"
# https://github.com/koalaman/shellcheck/wiki/SC1090
# shellcheck disable=SC1090
. "${PROFILE_PYTHON}"

brew install "python@${BREW_PY}"
brew install pipx

pipx install poetry

# Node
# -----------------------------------------------------------------------------

brew install node
npm install -g npm

#  Development tools
# -----------------------------------------------------------------------------

brew install gh
brew install act

brew install editorconfig
brew install prettier

brew install hadolint
npm install -g dockerfilelint

brew install shfmt
brew install checkbashisms
brew install shellcheck

brew install markdownlint-cli
brew install lychee

npm install -g cspell
brew install get-woke/tap/woke

brew install pandoc
brew install tidy-html5

# Clean up
# -----------------------------------------------------------------------------

npm dedupe
npm prune
rm "${HOME}/package-lock.json"

brew cleanup -s
