#!/bin/bash
BASEDIR=$(dirname $0)
cd $BASEDIR

cd ../src

nohup python scheduler.py >/dev/null 2>&1 &