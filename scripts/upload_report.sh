#!/bin/bash

su ec2-user
aws s3 cp s3://awscsp1337/dd_upload_script.zip .
unzip -o dd_upload_script.zip && mv dd_upload_script/* .
pip install -r requirements.txt
python dd_upload.py 
