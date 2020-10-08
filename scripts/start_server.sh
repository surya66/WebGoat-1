#!/bin/bash
echo "export WEBGOAT_HOST=$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)" >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc
echo "export WEBGOAT_HOST=$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)" >> ~/.bashrc
source ~/.bashrc

if echo $(sudo lsof -t -i:1337); then kill $(sudo lsof -t -i:1337); fi

java -jar /tmp/webgoat-server-v8.1.0.jar --server.port=1337 --server.address=$WEBGOAT_HOST  >/dev/null 2>&1 &