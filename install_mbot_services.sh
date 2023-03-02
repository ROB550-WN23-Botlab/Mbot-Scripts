#!/usr/bin/bash
sudo cp mbot_startup.service /etc/systemd/system/mbot_startup.service
sudo cp mbot_ip_git.service /etc/systemd/system/mbot_ip_git.service
sudo systemctl daemon-reload
