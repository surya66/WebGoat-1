#!/bin/bash
sleep 1m
cd /tmp
sudo docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t http://$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1):1337/WebGoat/login -g gen.conf -x ZAP-Scan.xml >/dev/null 2>&1 &
sudo docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t http://$(ip -f inet -o addr show eth0 | awk '{print $4}' | cut -d '/' -f 1):1337/WebGoat/login -g gen.conf -r ZAP-Scan.html >/dev/null 2>&1 &
cd -
