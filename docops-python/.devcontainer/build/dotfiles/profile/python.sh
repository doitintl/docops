# shellcheck shell=sh

export BREW_PY="3.9"

export BREW_PREFIX="$(brew --prefix)"

export PATH="${BREW_PREFIX}/opt/python@${BREW_PY}/libexec/bin:${PATH}"
export PATH="${BREW_PREFIX}/opt/python@${BREW_PY}/bin:${PATH}"

export LDFLAGS="-L${BREW_PREFIX}/opt/python@${BREW_PY}/lib"
export CPPFLAGS="-I${BREW_PREFIX}/opt/python@${BREW_PY}/include"
export PKG_CONFIG_PATH="${BREW_PREFIX}/opt/python@${BREW_PY}/lib/pkgconfig"
