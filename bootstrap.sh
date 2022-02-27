#!/bin/sh -ex
# shellcheck disable=SC2086

# POSIX locale
LC_ALL=C
export LC_ALL

DEBIAN_FRONTEND=noninteractive
export DEBIAN_FRONTEND

APT_GET_OPTS='-y --no-install-recommends'

apt-get update
apt-get install ${APT_GET_OPTS} build-essential

echo finished
