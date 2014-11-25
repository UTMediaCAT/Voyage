#!/bin/bash 
url=$1
BASEDIR=$(dirname $0) 
cd ..
mkdir -p $4
cd $4
wget $url --warc-file=$2 2> /dev/null
rm $2'.warc.gz' 2> /dev/null
if [ -f $2'.html' ]:
then
    cp -fp $3 $2'.html' 2> /dev/null
else
    mv $3 $2'.html' 2> /dev/null
fi
