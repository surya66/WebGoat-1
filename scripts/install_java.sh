#!/bin/bash
# sudo amazon-linux-extras install java-openjdk11 -y
sudo yum -y install docker
sudo service docker restart
echo 'export WEBGOAT_HOST=$(ip -f inet -o addr show en0 | awk '{print $4}' | cut -d '/' -f 1)' >> ~/.bashrc
source ~/.bashrc
