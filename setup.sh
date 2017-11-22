#!/bin/bash

set -e

scp -r . root@recalbox:~/retrogear

ssh -q root@recalbox "
    mount -o remount,rw /boot
    mount -o remount, rw /recalbox
    cp retrogear/boot.config /boot/config.txt
    cp retrogear/recalbox.conf recalbox.conf
    cp retrogear/volume-monitor.py /recalbox/scripts/volume-monitor.py
    cp retrogear/custom.sh custom.sh
    rm -Rf retrogear
    reboot -h
"
