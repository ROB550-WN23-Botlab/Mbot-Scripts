#!/usr/bin/python3
import os
import time
# Define the path to the config file
config_file = "/boot/firmware/mbot_config.txt"

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

# Check if there is an active WiFi connection
wifi_active = False
wifi_status = os.popen("nmcli -t -f NAME,DEVICE,STATE c show --active").read().strip()
if wifi_status:
    for line in wifi_status.split('\n'):
        name, device, state = line.split(':')
        if device == 'wlan0' and state == 'activated' and name != 'mbot_wifi_ap':
            wifi_active = True
            break

if wifi_active:
    # Already connected to  WiFi network
    print("Connected to a WiFi network... Done.")
else:
    print("No connection active, attempting to connect to home network...")
    # check if we see our home wifi network
    available_networks = []
    known_networks = []
    scan_output = os.popen("sudo nmcli dev wifi list").read().split('\n')
    for line in scan_output:
        if len(line.strip()) > 0 and not line.startswith("IN-USE"):
            available_networks.append(line.strip().split()[1])
    if home_wifi_ssid in available_networks:
        print("Found WiFi network, checking for network profile...")
        output = os.popen("nmcli connection show").read().split('\n')
        for line in output:
            if len(line.strip()) > 0:
                known_networks.append(line.strip().split()[0])
        if home_wifi_ssid in known_networks:
            print("Found network profile. Connecting...")
            # Connect to home WiFi network
            os.system(f"sudo nmcli connection up '{home_wifi_ssid}'")
            print("Connected to home WiFi network.")
        else:
            print("No network profile found. Adding new profile...")
            # Adding network config and connecting
            os.system(f"sudo nmcli connection add type wifi ifname wlan0 con-name '{home_wifi_ssid}' autoconnect yes ssid '{home_wifi_ssid}'")
            os.system(f"sudo nmcli connection modify '{home_wifi_ssid}' wifi-sec.key-mgmt wpa-pask")
            os.system(f"sudo nmcli connection modify '{home_wifi_ssid}' wifi-sec.psk '{home_wifi_password}'")
            os.system(f"sudo nmcli connection up '{home_wifi_ssid}'")
            print("Connected to home WiFi network.")
        wifi_active = True
    else:
        print("No connections available. Starting Wifi AP...")
        # Check if the access point already exists
        ap_exists = False
        for line in os.popen("nmcli connection show").readlines():
            if "mbot_wifi_ap" in line:
                ap_exists = True
                break

        if not ap_exists:
            print("Access point profile does not exist. Creating now...")
            # Configure Network Manager to create a WiFi access point
            os.system(f"sudo nmcli connection add type wifi ifname '*' con-name mbot_wifi_ap autoconnect no ssid {ap_ssid}")
            os.system("sudo nmcli connection modify mbot_wifi_ap 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared")
            os.system(f"sudo nmcli connection modify mbot_wifi_ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk {ap_password}")
            os.system("sudo nmcli connection modify mbot_wifi_ap ipv4.address 192.168.1.1/24 ipv4.gateway 192.168.1.1")
            time.sleep(10.0)
            os.system("sudo nmcli connection up mbot_wifi_ap")
            print("Access point created successfully.")
        else:
            print("Access point profile already exists...")
            os.system("sudo nmcli connection up mbot_wifi_ap")
            print("Access point created successfully.")
if wifi_active == True:
    os.system("/home/pi/Installers/update_IP.sh")
