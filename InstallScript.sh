#!/bin/bash
set -e

apt-get update
apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev python3-pip phantomjs libmysqlclient-dev

pip install -r requirements.txt
pip3 install wpull

dir=`pwd`
sed 's#projectdir:.*$#projectdir: '"${dir}"'#' config.yaml > tmp.yaml
mv tmp.yaml config.yaml
mkdir log
