#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd crawler
python crawler.py -u $1
cd ..
cd ..
mkdir -p warc
mv ./src/crawler/out.warc.gz ./warc/
cd ./warc 
mv out.warc.gz $2'.warc.gz'
