#!/bin/bash
kill -9 $(lsof -i:$1 -t) 2> /dev/null
kill -9 $(lsof -i:$2 -t) 2> /dev/null
