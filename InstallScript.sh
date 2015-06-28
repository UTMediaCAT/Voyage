#!/bin/bash
set -e

apt-get update
apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev wget

pip install -r requirements.txt
