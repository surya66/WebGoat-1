#!/bin/bash

aws s3 cp s3://awscsp1337/dd_upload_script.zip .
unzip -o dd_upload_script.zip && mv dd_upload_script/* .
python dd_upload.py
