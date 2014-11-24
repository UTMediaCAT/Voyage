#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd crawler
python crawler.py -u $1
cd ..
cd ..
mkdir -p warc
mkdir -p warc/$3
mv ./src/crawler/out.warc.gz ./warc/$3
cd ./warc/$3 
mv out.warc.gz $2'.warc.gz'
