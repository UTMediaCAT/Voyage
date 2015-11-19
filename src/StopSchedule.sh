#!/bin/bash

kill -9 `ps -aux | grep -v grep |grep  "scheduler.py" |awk '{ print $2 }'`
