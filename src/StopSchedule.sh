#!/bin/bash
pkill python scheduler.py




kill -9 `ps | grep -v grep |grep  "scheduler.py" |awk '{ print $1 }'`