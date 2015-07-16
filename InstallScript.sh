#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev

sudo pip install -r requirements.txt

dir=`pwd`
sed 's#projectdir:.*$#projectdir: '"${dir}"'#' config.yaml > tmp.yaml
mv tmp.yaml config.yaml
mkdir log