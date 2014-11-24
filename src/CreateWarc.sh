#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd ..
mkdir -p warc
mkdir -p warc/$3
cd warc/$3
wget $url --warc-file=$2
rm index.html 2> /dev/null 
