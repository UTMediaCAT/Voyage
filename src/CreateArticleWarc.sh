#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd ..
mkdir -p $3
cd $3
wget $url --warc-file=$2
rm index.html 2> /dev/null 
