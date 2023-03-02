#!/usr/bin/bash
sudo cp mbot_start_network.service /etc/systemd/system/mbot_start_network.service
sudo cp mbot_publish_info.service /etc/systemd/system/mbot_publish_info.service
sudo systemctl daemon-reload
