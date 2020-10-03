#!/bin/bash
# sudo amazon-linux-extras install java-openjdk11 -y
sudo yum -y install docker
sudo service docker restart
echo "export WEBGOAT_HOST=$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)" >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc
