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
        if device == 'wlan0' and state == 'activated':
            wifi_active = True
            break

if wifi_active:
    # Already connected to  WiFi network
    print("Connected to a WiFi network... Done.")
else:
    available_networks = []
    scan_output = os.popen("sudo nmcli dev wifi list").read().split('\n')
    for line in scan_output:
        if len(line.strip()) > 0 and not line.startswith("IN-USE"):
            available_networks.append(line.strip().split()[0])
            print(line.strip().split()[0])
    home_wifi_exists = False
    if home_wifi_ssid in available_networks:
        # Set up home WiFi connection  
        for line in os.popen("nmcli connection show").readlines():
            print(line)
            if home_wifi_ssid in line:
                home_wifi_exists = True
                break

    if home_wifi_exists:
        # Connect to home WiFi network
        os.system(f"sudo nmcli connection up '{home_wifi_ssid}' password '{home_wifi_password}'")
        print("Connected to home WiFi network.")
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
            print("Access point created successfully.")
        else:
            print("Access point already exists, not created.")

        # Turn on WiFi radio
        os.system("sudo nmcli radio wifi on")
