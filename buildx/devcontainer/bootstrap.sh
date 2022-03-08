#!/bin/sh -ex
# shellcheck disable=SC2086

# POSIX locale
LC_ALL=C
export LC_ALL

DEBIAN_FRONTEND=noninteractive
export DEBIAN_FRONTEND

APT_GET_OPTS='-y --no-install-recommends'

apt-get update

# https://www.gnu.org/software/make/
apt-get install ${APT_GET_OPTS} make make-doc
