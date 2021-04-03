#!/bin/bash

/usr/bin/qemu-system-x86_64 \
	-kernel ./bzImage \
	-initrd $PWD/initramfs.cpio-peserta.gz \
	-nographic \
	-monitor none \
	-append "console=ttyS0 nokaslr nopti root=/dev/ram rw"
