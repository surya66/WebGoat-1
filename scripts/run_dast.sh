#!/bin/bash
sleep 2m
cd /tmp
sudo docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t http://$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1)/WebGoat/login -g gen.conf -x zap_testreport.xml
