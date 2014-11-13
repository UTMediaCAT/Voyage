#!/bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

cd ../Frontend
python manage.py runserver