#!/bin/bash

# Set the name of the access point connection
ap_name="mbotAP"

# Check if the access point connection is already active
if nmcli connection show --active | grep -q "$ap_name"; then
    echo "Access point connection $ap_name is already active"
    exit 0
fi

# Check if any known networks are available
known_networks=$(nmcli device wifi list | grep -v "^*")
if [[ -n "$known_networks" ]]; then
    echo "Known networks are available, not starting access point"
    exit 0
fi

# Start the access point connection
echo "Starting access point connection $ap_name"
nmcli connection up "$ap_name"
