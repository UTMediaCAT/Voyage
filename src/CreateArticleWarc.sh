#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd ..
mkdir -p $3
cd $3
wget $url --warc-file=$2 2> /dev/null 
find .  -maxdepth 1 -type f ! -iname "*.warc.gz" -delete 2> /dev/null 
