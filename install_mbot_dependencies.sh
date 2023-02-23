#!/bin/bash

#### Variables ####
user="pi"

#### Install software from apt-get ####
apt-get update
apt-get upgrade -y
apt-get -y install raspi-config openssh-server
apt-get -y install git software-properties-common apt-transport-https wget gpg

apt-get -y install build-essential wget dkms \
    autoconf automake autotools-dev gdb libglib2.0-dev libgtk2.0-dev \
    libusb-dev libusb-1.0-0-dev freeglut3-dev libboost-dev libatlas-base-dev \
    libgsl-dev libjpeg-dev default-jdk doxygen openssl libssl-dev libdc1394-dev \
    libcamera-dev v4l-utils

apt-get -y install mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev

apt-get -y install python3-dev python3-numpy python3-matplotlib python3-opencv python3-scipy cython3 python3-picamera

apt-get -y install gcc-arm-none-eabi libnewlib-arm-none-eabi

#### Enable features for raspi ####
raspi-config nonint do_vnc 0
raspi-config nonint do_ssh 0
raspi-config nonint do_camera 0

mkdir /home/$user/Installers
cd /home/$user/Installers

#### Downgrade CMake to work with botlab ####
apt-get remove cmake
apt-get purge --auto-remove cmake
wget http://www.cmake.org/files/v3.17/cmake-3.17.3.tar.gz
tar -xf cmake-3.17.3.tar.gz
cd cmake-3.17.3
./configure
make && make install 


#### Install VSCode from Microsoft ####
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list
apt update
apt install code

#### Install LCM ####
cd /home/$user/Installers
git clone https://github.com/lcm-proj/lcm.git /home/$user/lcm
mkdir /home/$user/Installers/lcm/build
cd /home/$user/Installers/lcm/build
cmake /home/$user/Installers/lcm
make && make install
cd /home/$user/Installers/lcm/lcm-python
python3 setup.py install

#### Install pico tools ####
cd /home/$user
wget https://raw.githubusercontent.com/raspberrypi/pico-setup/master/pico_setup.sh
chmod +x pico_setup.sh
./pico_setup.sh

git clone https://github.com/raspberrypi/pico-sdk.git
git clone https://github.com/raspberrypi/pico-examples.git
cd pico-sdk
git submodule --init
cd /home/$user

echo "Done Installing!"
