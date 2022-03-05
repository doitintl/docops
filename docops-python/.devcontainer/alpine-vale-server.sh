#!/bib/sh -e

tmpdir=$(mktemp -d)

cd "${tmpdir}"

# While I experiment, I want my files to persist between restarts
cd /root

cat >/etc/apk/repositories <<EOF
https://dl-cdn.alpinelinux.org/alpine/edge/main
https://dl-cdn.alpinelinux.org/alpine/edge/testing
https://dl-cdn.alpinelinux.org/alpine/edge/community
EOF

apk update
apk upgrade

# Needed by default
apk add --no-cache \
    alpine-sdk \
    util-linux

# Needed to read the AppImage, but still produces an error about squashfs
apk add gcompat

# Experimental
apk add squashfs-tools fuse

wget https://github.com/errata-ai/vale-server/releases/download/v2.0.0/Vale-Server-2.0.0-linux.AppImage
chmod 755 Vale-Server-2.0.0-linux.AppImage

./Vale-Server-2.0.0-linux.AppImage --appimage-extract
# This doesn't look like a squashfs image.
# Failed to open squashfs image

apk add xpra

# temp experiment, building from source
# - download source from https://github.com/probonopd/linuxdeployqt/releases
# - use the BUILDING.md file as a guide

wget https://github.com/probonopd/linuxdeployqt/archive/refs/tags/continuous.tar.gz
tar -xvzf continuous.tar.gz
code linuxdeployqt-continuous/BUILDING.md

wget https://github.com/errata-ai/vale-server/archive/refs/tags/v2.0.0.tar.gz
tar -xvzf v2.0.0.tar.gz

# from https://github.com/errata-ai/vale-server/blob/master/pkg/linux/Makefile
# rm -rf *.AppImage
# cp \
#     '/home/jdkato/Desktop/Git/build-systray-Desktop_Qt_5_15_2_GCC_64bit-Release/Vale Server' \
#     vale-server/usr/bin/vale-server
# linuxdeployqt \
#     vale-server/usr/share/applications/vale-server.desktop \
#     -appimage \
#     -no-translations \
#     -bundle-non-qt-libs \
#     -extra-plugins=imageformats,iconengines,platformthemes/libqgtk3.so \
#     -always-overwrite -qmake=/home/jdkato/Qt/5.15.2/gcc_64/bin/qmake

apk add g++
apk add mesa-gl
apk add mesa-dev
apk add mesa-gles
apk add mesa-glapi

# remove this, as the packaged glibc overwrites its files and produces an error
apk del gcompat
# https://github.com/sgerrand/alpine-pkg-glibc/
wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-2.34-r0.apk
apk add glibc-2.34-r0.apk

# In case you get errors
apk fix

# set up locales
wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-bin-2.34-r0.apk
wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-i18n-2.34-r0.apk
apk add glibc-bin-2.34-r0.apk glibc-i18n-2.34-r0.apk
/usr/glibc-compat/bin/localedef -i en_US -f UTF-8 en_US.UTF-8

apk add qt5-qtbase
apk add qt5-qtbase-dev

qmake-qt5
make

apk add python3
apk add py3-pip
apk add py3-netifaces
apk add py3-xdg
apk add py3-uinput

pip3 install paramiko
pip3 install pyinotify

apk add cairo

apk add dbus
apk add dbus-x11

apk add linux-edge
ln -s /lib/modules/5.16.7-0-edge /lib/modules/5.4.0-1067-azure
resart

apk add eudev
apk add lxc
apk add openrc
rc-update add udev
rc-update add cgroups
echo "lxc.cgroup.use = @kernel" >> /etc/lxc/default.conf
reboot
rc-service udev start
# /lib/rc/sh/openrc-run.sh: line 108: can't create /sys/fs/cgroup/blkio/tasks: Read-only file system
# /lib/rc/sh/openrc-run.sh: line 108: can't create /sys/fs/cgroup/cpu/tasks: Read-only file system


xpra start \
    --bind-tcp=0.0.0.0:10000 \
    --html=on \
    --start-child='./Vale\ Server' \
    --exit-with-children \
    --daemon=no \
    --opengl=no \
    --resize-display=yes \
    --pulseaudio=no \
    --notifications=no \
    --bell=no \
    --webcam=no \
    --mdns=no \
    --xvfb="Xvfb -nolisten tcp -noreset"
