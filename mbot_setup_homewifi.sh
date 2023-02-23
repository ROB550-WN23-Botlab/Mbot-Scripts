MyWifi="MyWifi"
MyWifiPassword="MyWifiPassword"

sudo nmcli connection add type wifi ifname wlan0 con-name $MyWifi autoconnect yes ssid $MyWifi
sudo nmcli connection modify $MyWifi wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify $MyWifi wifi-sec.psk $MyWifiPassword
nmcli connection modify $MyWifi connection.autoconnect-priority 5