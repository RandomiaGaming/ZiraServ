#!/usr/bin/bash

if [ -z "$ALACRITTY_WINDOW_ID" ] && [[ "$1" != "alacritty" ]]; then
    exec alacritty -e bash "$0" "alacritty"
fi

if [[ "$(id -u)" != "0" ]]; then
    exec sudo "$0" "alacritty"
fi

umount ./mount
rm -rf ./mount

mkdir -p ./mount
mount -o loop,offset=53477376,rw disk.img ./mount

echo Mounted device press any key to umount...
read

umount ./mount
rm -rf ./mount