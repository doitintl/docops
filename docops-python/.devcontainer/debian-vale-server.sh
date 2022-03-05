DEBIAN_FRONTEND=noninteractive
export DEBIAN_FRONTEND

apt-get update
apt-get upgrade

cd /root

# -----------------------------------------------------------------------------

VALE_BIN='vale'
VALE_VERS='2.14.0'
VALE_PKG="${VALE_BIN}_${VALE_VERS}_Linux_64-bit"
VALE_TGZ="${VALE_PKG}.tar.gz"
VALE_SIG="${VALE_BIN}_${VALE_VERS}_checksums.txt"

VALE_REPO_URL="https://github.com/errata-ai/vale"
VALE_RELEASE_URL="${VALE_REPO_URL}/releases/download/v${VALE_VERS}"
VALE_SIG_URL="${VALE_RELEASE_URL}/${VALE_SIG}"
VALE_TGZ_URL="${VALE_RELEASE_URL}/${VALE_TGZ}"

curl -fsSL "${VALE_SIG_URL}" >"${VALE_SIG}"
curl -fsSL "${VALE_TGZ_URL}" >"${VALE_TGZ}"

sha256sum --check --ignore-missing "${VALE_SIG}"

tar -xzf "${VALE_TGZ}"
chown root:root "${VALE_BIN}"
chmod 755 "${VALE_BIN}"
mv "${VALE_BIN}" /usr/local/bin

# -----------------------------------------------------------------------------

wget https://github.com/errata-ai/vale-server/releases/download/v2.0.0/Vale-Server-2.0.0-linux.AppImage
chmod 755 Vale-Server-2.0.0-linux.AppImage
./Vale-Server-2.0.0-linux.AppImage --appimage-extract
chown -R root squashfs-root/
mv squashfs-root /usr/local/vale-server
ln -s /usr/local/vale-server/usr/bin/vale-server /usr/local/bin

apt-get install -y libgl1
apt-get install -y libglib2.0-0

apt-get install -y xpra

apt-get install -y dbus-x11

mkdir -p /run/user/1000
chown -R 1000 /run/user/1000

mkdir -p /run/xpra
chown -R 1000 /run/xpra

apt-get install -y python3-pip
apt-get install -y python3-pyinotify

apt-get install -y menu-xdg
# Run as vscode
# -----------------------------------------------------------------------------

# perhaps not needed
xpra start \
    --start-child='setxkbmap us' \
    --exit-with-children \
    --daemon=no \
    --opengl=no \
    --resize-display=yes \
    --pulseaudio=no \
    --notifications=no \
    --bell=no \
    --webcam=no \
    --mdns=no

xpra start \
    --bind-tcp=0.0.0.0:10000 \
    --html=on \
    --start-child='vale-server' \
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

# works!
