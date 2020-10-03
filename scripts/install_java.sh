#!/bin/bash
sudo yum install java -y
sudo yum -y install docker
sudo service docker restart
echo "export WEBGOAT_HOST=$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)" >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc
echo "export WEBGOAT_HOST=$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)" >> ~/.bashrc
source ~/.bashrc
#kill $(lsof -ti :80) >/dev/null 2>&1 &
