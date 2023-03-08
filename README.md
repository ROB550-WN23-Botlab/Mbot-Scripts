This repository has helper scripts for setting up and running the MBot

There are 2 services that must be running,

`mbot_start_networking.service`
- will set up networking in the following way:
    - Set the hostname based on /boot/mbot_config.txt which resides on the FAT32 partition and can be 
        mounted and modified by the user
    - If a connection is already made, (i.e. MWireless) do nothing
    - If a connection doesnt exist, try to setup home wifi net from the /boot/mbot_config.txt
    - If a connection cannot be made, start the access point based on /boot/mbot_config.txt

`mbot_publish_info.service`:
- runs after networking is set up.  It will clone the MBot IP address repository, update the json file based on the hostname, add the IP address and push the repo to gitlab.

first, update `mbot_config.txt` with your relevant information:
1. The `mbot_hostname` is `mbot-XXX`, which should be determined by the number on the robot
2. The `mbot_ap_password` field is what you will enter as the password to the AP if needed
3. The `home_wifi_ssid` field is your home network name (i.e. what what would appear on the list of available networks).
4. The `home_wifi_password` field is the password to your home network. Make sure not to push your changes if you update this!!!

Then install:
```
$ cd mbot_scripts
$ git submodule init
$ git submodule update
$ cd mbot-ip
$ git checkout master
$ cd ..
$ sudo ./install_mbot_services.sh
```

You can additionally install the server for remote desktoping into the Pi by installing NoMachine:
```
$ sudo ./install_nomachine.sh
```
