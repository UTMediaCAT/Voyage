#!/bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

cd warc_proxy
python warcproxy.py