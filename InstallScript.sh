#!/bin/bash

prevdir=$pwd
cd ~
wget 'http://bootstrap.pypa.io/get-pip.py'
python get-pip.py --user
rm get-pip.py
cd $prevdir

pip install --user Django==1.7.1
pip install --user newspaper==0.0.8
pip install --user tweepy==2.3.0
pip install --user python-dateutil==1.5
pip install --user tld==0.7.2
pip install --user pyyaml==3.11
pip install --user django-suit==0.2.11
