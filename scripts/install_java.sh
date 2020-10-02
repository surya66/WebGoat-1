#!/bin/bash
# sudo amazon-linux-extras install java-openjdk11 -y
sudo yum -y install docker
sudo service docker restart
export WEBGOAT_HOST=$(ip -f inet -o addr show docker0 | awk '{print $4}' | cut -d '/' -f 1)
