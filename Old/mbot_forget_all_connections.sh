#!/bin/bash

# Get a list of all connections and their UUIDs
connections=$(nmcli connection show | awk 'NR>1{print $1}')

# Iterate through list of WiFi connection names
for connection in $connections
do
  # Skip over the "Wired" connection
  if [ "$connection" = "Wired" ]; then
    echo "Skipping Wired connection"
    continue
  fi
  
  echo "Deleting WiFi connection: $connection"
  nmcli connection delete $connection
done