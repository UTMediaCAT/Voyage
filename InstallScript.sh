#!/bin/bash

# Install apt dependencies
apt-get install python
pip install --upgrade pip==9.0.0
apt-get update && apt-get install -y python-dev python-pip python3-pip python-numpy zlib1g-dev libxml2-dev libxslt-dev libjpeg-dev libpq-dev libfontconfig postgresql postgresql-contrib language-pack-en htop lsof
apt-get autoremove -y python-setuptools

# Install python dependencies:
pip install -U pip setuptools
# Install nltk before installing the newspaper package in requirements to avoid error 
pip install https://s3-us-west-2.amazonaws.com/jdimatteo-personal-public-readaccess/nltk-2.0.5-https-distribute.tar.gz
pip install -r requirements.txt
pip3 install wpull
pip3 install html5lib==0.9999999
pip3 install psutil

# Install phantomjs
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
mv -f phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
rm -rf phantomjs-2.1.1-linux-x86_64
rm phantomjs-2.1.1-linux-x86_64.tar.bz2

# Set up
set -e

dir=`pwd`
sed 's#projectdir:.*$#projectdir: '"${dir}"'#' config.yaml > tmp.yaml
mv tmp.yaml config.yaml
mkdir -p log
