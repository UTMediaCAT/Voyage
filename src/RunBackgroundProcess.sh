#!/bin/bash
BASEDIR=$(dirname $0)
cd $BASEDIR

cd ../src


nohup python warc_queue.py &