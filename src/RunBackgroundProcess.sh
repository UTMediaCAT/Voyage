#!/bin/bash
BASEDIR=$(dirname $0)
cd $BASEDIR

cd ../src


nohup python3 warc_queue.py >/dev/null 2>&1 &