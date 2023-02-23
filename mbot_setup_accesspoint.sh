mbot_hostname=$(hostname)
MyAccessPoint="$mbot_hostname-AP"
MyPassword="iloverobots"
sudo nmcli connection add type wifi ifname '*' con-name $MyAccessPoint autoconnect no ssid $MyAccessPoint
sudo nmcli connection modify $MyAccessPoint 802-11-wireless.mode ap 802-11-wireless.band ac ipv4.method shared
sudo nmcli connection modify $MyAccessPoint wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify $MyAccessPoint wifi-sec.psk MyPassword
sudo nmcli connection modify $MyAccessPoint connection.autoconnect-priority 10