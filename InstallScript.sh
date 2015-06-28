#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev wget

sudo pip install -r requirements.txt
