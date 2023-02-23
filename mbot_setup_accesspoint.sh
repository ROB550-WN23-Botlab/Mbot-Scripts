#!/bin/bash
MBotHostname=$(hostname)
MyAccessPoint="mbotAP"
MyAccessPointSSID="$MBotHostname-AP"
MyPassword="iloverobots"
sudo nmcli connection add type wifi ifname '*' con-name $MyAccessPoint autoconnect no ssid $MyAccessPointSSID
sudo nmcli connection modify $MyAccessPoint 802-11-wireless.mode ap 802-11-wireless.band a ipv4.method shared
sudo nmcli connection modify $MyAccessPoint wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify $MyAccessPoint wifi-sec.psk MyPassword
sudo nmcli connection modify $MyAccessPoint connection.autoconnect-priority 10