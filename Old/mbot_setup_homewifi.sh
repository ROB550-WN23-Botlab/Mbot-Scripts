# Prompt the user for the Wi-Fi SSID
read -p "Enter the Wi-Fi SSID: " MyWifi

# Prompt the user for the Wi-Fi password, hiding the input
read -s -p "Enter the Wi-Fi password: " MyWifiPassword
echo ""

sudo nmcli connection add type wifi ifname wlan0 con-name $MyWifi autoconnect yes ssid $MyWifi
sudo nmcli connection modify $MyWifi wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify $MyWifi wifi-sec.psk $MyWifiPassword
nmcli connection modify $MyWifi connection.autoconnect-priority 5

echo "Connection Saved"