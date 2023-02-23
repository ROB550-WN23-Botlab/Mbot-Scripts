#!/bin/bash

# Get a list of all connections and their UUIDs
connections=$(nmcli connection show | awk '{print $2}')

# Loop through the connections and forget them
for conn in $connections; do
    nmcli connection delete uuid "$conn"
done
