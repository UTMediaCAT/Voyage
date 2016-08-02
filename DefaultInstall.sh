#!/bin/bash
# Install apt dependencies
apt-get update && apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev python-psycopg2 libjpeg-dev python3-pip phantomjs postgresql postgresql-contrib

#Install python dependencies:
pip install -r requirements.txt
pip3 install wpull

# Set up
set -e

dir=`pwd`
sed 's#projectdir:.*$#projectdir: '"${dir}"'#' config.yaml > tmp.yaml
mv tmp.yaml config.yaml
mkdir -p log
