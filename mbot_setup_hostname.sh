#!/bin/bash

if [ $# -eq 0 ];
then
  echo "$0: Missing arguments"
  exit 1
elif [ $# -gt 1 ];
then
  echo "$0: Too many arguments: $@"
  exit 1
else

#### Variables ####
hostname="$1"

#### Set hostname, timezone and keyboard ####
hostnamectl set-hostname $hostname
sed -i "s/raspberrypi/$hostname/g" /etc/hostname
sed -i "s/raspberrypi/$hostname/g" /etc/hosts
bash -c "echo America/Detroit > /etc/timezone"
sed -i "s/gb/us/g" /etc/default/keyboard

echo "Done Setting Hostname!"
fi