#!/bin/bash
# sudo amazon-linux-extras install java-openjdk11 -y
sudo yum -y install docker
sudo service docker restart
echo 'export WEBGOAT_HOST=172.17.0.1' >> ~/.bashrc
source ~/.bashrc
