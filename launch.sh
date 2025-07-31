#!/bin/sh

if [[ ! -f "disk.img" ]]; then
  dd if=/dev/zero of=disk.img bs=1G count=64 status=progress
fi

qemu-system-x86_64 \
  -enable-kvm \
  -cpu host \
  -smp cores=4 \
  -m 4G \
  -drive file=./disk.img,format=raw \
  -cdrom ./win10.iso \
  -display sdl -vga std \
  -audiodev pa,id=snd0,out.frequency=48000 -device ich9-intel-hda -device hda-output,audiodev=snd0 \
  -device rtl8139,netdev=net0 -netdev user,id=net0,hostfwd=tcp::41875-:41875 \
  -name "TTSVM"