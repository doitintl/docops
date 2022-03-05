#!/bin/sh -ex

# POSIX locale
LC_ALL=C
export LC_ALL

if command -v npm >/dev/null; then
    npm dedupe
    npm prune
    npm cache clean --force
fi

apt-get clean
apt-get auto-remove
rm -rf /var/lib/apt/lists/*
