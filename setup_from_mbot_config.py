#!/usr/bin/python3
import os
import time
# Define the path to the config file
config_file = "/boot/firmware/mbot_config.txt"

# Define the path to the log file
log_file = "/var/log/mbot_config.log"

with open(log_file, "a") as log:
    log.write(f"'{time.date()}'\n")
    # Read the config file and store the values in variables
    with open(config_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.strip().split("=")
            if key == "mbot_hostname":
                hostname = value
            elif key == "mbot_ap_ssid":
                ap_ssid = value
            elif key == "mbot_ap_password":
                ap_password = value
            elif key == "home_wifi_ssid":
                home_wifi_ssid = value
            elif key == "home_wifi_password":
                home_wifi_password = value

    # Set hostname immediately
    os.system(f"hostnamectl set-hostname {hostname}")
    # Set the hostname in /etc/hostname
    with open("/etc/hostname", "w") as f:
        f.write(hostname)
    # Change the hostname in /etc/hosts
    with open("/etc/hosts", "r") as f:
        filedata = f.read()
        filedata = filedata.replace(os.uname()[1], hostname)
    with open("/etc/hosts", "w") as f:
        f.write(filedata)
    log.write(f"hostname set to '{hostname}'\n")

    # Check if there is an active WiFi connection
    wifi_active = False
    wifi_status = os.popen("nmcli -t -f NAME,DEVICE,STATE c show --active").read().strip()
    if wifi_status:
        for line in wifi_status.split('\n'):
            name, device, state = line.split(':')
            if device == 'wlan0' and state == 'activated':
                wifi_active = True
                break

    if wifi_active:
        # Already connected to  WiFi network
        log.write(f"Connected to WiFi network '{name}'. Done.\n")
    else:
        # We don't have a wifi network, check for ones we know
        available_networks = []
        known_networks = []
        scan_output = os.popen("sudo nmcli dev wifi list").read().split('\n')
        for line in scan_output:
            if len(line.strip()) > 0 and not line.startswith("IN-USE"):
                ssid = line.strip().split()[1]
                if ssid not in availabe_networks:
                    available_networks.append(ssid)
        log.write(available_networks)
        
        home_wifi_exists = False
        if home_wifi_ssid in available_networks:
            # Set up home WiFi connection  
            for line in os.popen("nmcli connection show").readlines():
                log.write(line)
                if home_wifi_ssid in line:
                    home_wifi_exists = True

        if home_wifi_exists:
            # Connect to home WiFi network
            os.system(f"sudo nmcli connection up '{home_wifi_ssid}' password '{home_wifi_password}'")
            log.write(f"Connected to WiFi network '{home_wifi_ssid}'. Done.\n")
        else:
            # Check if the access point already exists
            ap_exists = False
            for line in os.popen("nmcli connection show").readlines():
                if "mbot_wifi_ap" in line:
                    ap_exists = True
                    break

        if not ap_exists:
            # Configure Network Manager to create a WiFi access point
            os.system(f"sudo nmcli connection add type wifi ifname '*' con-name mbot_wifi_ap autoconnect no ssid {ap_ssid}")
            os.system("sudo nmcli connection modify mbot_wifi_ap 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared")
            os.system(f"sudo nmcli connection modify mbot_wifi_ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk {ap_password}")
            os.system("sudo nmcli connection modify mbot_wifi_ap ipv4.address 192.168.1.1/24 ipv4.dns '8.8.8.8 8.8.4.4'")
            time.sleep(10.0)
            os.system("sudo nmcli connection up mbot_wifi_ap")
            log.write("Access point created successfully. \n")
        else:
            log.write("Access point already exists, not created. \n")
