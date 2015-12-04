#!/bin/bash
kill -15 $(lsof -i:$1 -t) 2> /dev/null
