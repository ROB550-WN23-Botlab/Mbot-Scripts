#!/usr/bin/python3
import os
import time
import datetime 
# Define the path to the config file
config_file = "/boot/firmware/mbot_config.txt"

# Define the path to the log file
log_file = "/home/pi/mbot_scripts/log/mbot_start_networking.log"

host= 'google.com'

with open(log_file, "a") as log:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log.write("===== ")
    log.write(formatted_time)
    log.write(" =====\n")
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
        log.write(f"Connected to active WiFi network '{name}'. Done.\n")

    else:
        # We don't have a wifi network, check for ones we know
        available_networks = []
        known_networks = []
        bssid = []
        ssid = []
        channel = []
        signal = []
        log.write(f"Looking for home network '{home_wifi_ssid}'\n")
        log.write("Wifi Scan: ")
        scan_output = os.popen("nmcli dev wifi list").read().split('\n')
        for line in scan_output:
            if len(line.strip()) > 0 and not line.startswith("IN-USE"):
                if line.strip().split()[1] == home_wifi_ssid:
                    bssid.append(line.strip().split()[0])
                    ssid.append(line.strip().split()[1])
                    channel.append(line.strip().split()[3])
                    signal.append(line.strip().split()[6])
                    log.write(f"{line}\n")            
        log.write("\n")
        available = list(zip(bssid, ssid, channel, signal))
        sorted_avail = sorted(available, key=lambda x: (int(x[2]), int(x[3])), reverse=True)
        print(sorted_avail)
        if home_wifi_ssid in ssid:
            # Check if we've already added the home network 
            for line in os.popen("nmcli connection show").readlines():
                ssid = line.strip().split()[0]
                log.write(f"{ssid}, ")
                if ssid not in known_networks:
                    known_networks.append(ssid)
                    log.write(f"{ssid}, ")
            log.write("\n")
            if home_wifi_ssid not in known_networks:
                home_wifi_bssid = sorted_avail[0][0]
                # Connect to home WiFi network
                os.system(f"nmcli dev wifi connect '{home_wifi_bssid}' password '{home_wifi_password}'")
            else:
                os.system(f"nmcli connection up '{home_wifi_ssid}'")
            log.write(f"Started connection to WiFi network '{home_wifi_ssid}'. Done.\n")
            
        else:
            log.write("No networks found, starting Access Point\n")
            # Check if the access point already exists to delete, otherwise hostname may be wrong
            for line in os.popen("nmcli connection show").readlines():
                if "mbot_wifi_ap" in line:
                    log.write("Access point already exists, removing... \n")
                    os.system(f"nmcli connection delete mbot_wifi_ap")
                    break
            # Configure Network Manager to create a WiFi access point
            os.system(f"nmcli connection add type wifi ifname '*' con-name mbot_wifi_ap autoconnect no ssid {ap_ssid}")
            os.system("nmcli connection modify mbot_wifi_ap 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared")
            os.system(f"nmcli connection modify mbot_wifi_ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk {ap_password}")
            os.system("nmcli connection modify mbot_wifi_ap ipv4.address 192.168.1.1/24 ipv4.dns '8.8.8.8 8.8.4.4'")
            log.write("Access point created successfully. \n")
            time.sleep(10.0)
            os.system("nmcli connection up mbot_wifi_ap")
            log.write("Access point started successfully. \n")
