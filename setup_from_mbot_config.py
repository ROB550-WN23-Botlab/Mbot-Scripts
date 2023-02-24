import os

# Define the path to the config file
config_file = "/boot/firmware/mbot_config.txt"

# Read the config file and store the values in variables
with open(config_file, "r") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.strip().split("=")
        if key == "hostname":
            hostname = value
        elif key == "ssid":
            ssid = value
        elif key == "password":
            password = value
        elif key == "home_wifi_ssid":
            home_wifi_ssid = value
        elif key == "home_wifi_password":
            home_wifi_password = value

# Check if there is an active WiFi connection
wifi_status = os.popen("nmcli -t -f device,state dev wlan0").read().split(":")[1].strip()

if wifi_status == "connected"
    # Already connected to home WiFi network
    print("Connected to home WiFi network.")
else:
    # Set up home WiFi connection
    home_wifi_exists = False
    for line in os.popen("nmcli connection show").readlines():
        if home_wifi_ssid in line:
            home_wifi_exists = True
            break

    if home_wifi_exists:
        # Connect to home WiFi network
        os.system(f"sudo nmcli connection up '{home_wifi_ssid}' password '{home_wifi_password}'")
        print("Connected to home WiFi network.")
    else:
        # Set the hostname in /etc/hostname
        with open("/etc/hostname", "w") as f:
            f.write(hostname)

        # Change the hostname in /etc/hosts
        with open("/etc/hosts", "r") as f:
            filedata = f.read()

        filedata = filedata.replace(os.uname()[1], hostname)

        with open("/etc/hosts", "w") as f:
            f.write(filedata)

        # Check if the access point already exists
        ap_exists = False
        for line in os.popen("nmcli connection show").readlines():
            if "mbot_wifi" in line:
                ap_exists = True
                break

        if not ap_exists:
            # Configure Network Manager to create a WiFi access point
            os.system("sudo nmcli radio wifi off")
            os.system("sudo nmcli connection add type wifi ifname wlan0 con-name mbot_wifi ssid {ssid}")
            os.system(f"sudo nmcli connection modify mbot_wifi wifi.mode ap wifi.security.key-mgmt wpa-psk wifi.secur‌​ity-psk {password}")
            os.system("sudo nmcli connection up mbot_wifi")

            print("Access point created successfully.")
        else:
            print("Access point already exists, not created.")

        # Turn on WiFi radio
        os.system("sudo nmcli radio wifi on")
