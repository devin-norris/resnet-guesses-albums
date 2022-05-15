#!/bin/bash
cd /home/ec2-user/resnet-guesses-albums/
set -e
source env/bin/activate
python3 main.py
deactivate