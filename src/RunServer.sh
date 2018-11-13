#!/bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

cd ../Frontend
nohup python3 manage.py runserver $1 >/dev/null 2>&1 &
