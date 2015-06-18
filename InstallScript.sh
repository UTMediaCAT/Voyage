#!/bin/bash

set -e

apt-get update
apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev wget

pip install Django==1.7.1
pip install newspaper==0.0.8
pip install tweepy==2.3.0
pip install python-dateutil==1.5
pip install tld==0.7.2
pip install pyyaml==3.11
pip install django-suit==0.2.11
pip install pytz==2015.4
