#!/bin/sh -e

# TODO: Move all of this inside the `Dockerfile`
# This will allow me to take advantage of the `Dockerfile` linting tools

HOME="/home/vscode"

# Shell
# -----------------------------------------------------------------------------

BASHRC_DIRCOLORS="/tmp/build/dotfiles/bashrc/dircolors.sh"
BASHRC_PATH="/tmp/build/dotfiles/bashrc/path.sh"
PROFILE_BREW="/tmp/build/dotfiles/profile/brew.sh"
PROFILE_PYTHON="/tmp/build/dotfiles/profile/python.sh"

(echo && cat "${BASHRC_DIRCOLORS}") >>"${HOME}/.bashrc"
(echo && cat "${BASHRC_PATH}") >>"${HOME}/.bashrc"

# https://github.com/koalaman/shellcheck/wiki/SC1091
# shellcheck disable=SC1091
. "${HOME}/.bashrc"

# VS Code
# -----------------------------------------------------------------------------

VSCODE_CONFIG="${HOME}/.config/vscode-dev-containers"

# Disable first run notice message
mkdir -p "${VSCODE_CONFIG}"
touch "${VSCODE_CONFIG}/first-run-notice-already-displayed"

# Homebrew
# -----------------------------------------------------------------------------

GITHUB_BASE="https://raw.githubusercontent.com"
INSTALL_BREW="${GITHUB_BASE}/Homebrew/install/HEAD/install.sh"

cd "${HOME}"
curl -fsSL "${INSTALL_BREW}" >/tmp/install-homebrew.sh
chmod 755 /tmp/install-homebrew.sh
/tmp/install-homebrew.sh

# Configure the environment for Homebrew
(echo && cat "${PROFILE_BREW}") >>"${HOME}/.profile"
# https://github.com/koalaman/shellcheck/wiki/SC1090
# shellcheck disable=SC1090
. "${PROFILE_BREW}"

brew install gcc

# Python
# -----------------------------------------------------------------------------

# Set the Python version for install and copy it to `~/.profile` for use when
# configuring the Python environment
BREW_PY=3.9
(echo && echo "export BREW_PY=${BREW_PY}") >>"${HOME}/.profile"

brew install "python@${BREW_PY}"

# Configure the environment for Python
(echo && cat "${PROFILE_PYTHON}") >>"${HOME}/.profile"
# shellcheck disable=SC1090
. "${PROFILE_PYTHON}"

pip install --upgrade pip

pip install poetry

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
npm cache clean --force
rm "${HOME}/package-lock.json"

brew autoremove
rm -rf "$(brew --cache)"

# Removing this directory will significantly reduce the image size and not
# break any of the installed packages. However, doing so will essentially break
# Homebrew (as a package manager) inside the running container.
# rm -rf "$(brew--prefix)/Homebrew/Library/Taps"
