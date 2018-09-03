#!/bin/bash

# Uncomment the following loop if you experience freezing issues on your instance that is running MediaCat. This is a simple script that will forcibly restart the crawler every 2 days. There will be no data loss and the crawler will pick up where it left off after the restart. This is useful if you want to crawl many domains at once but do not have the resources for a pwerful server.
#while true
#do
#	python article_explorer.py &
#	sleep 2d
#	kill -15 `ps -aux | grep -v grep |grep  "article_explorer.py" |awk '{ print $2 }'`
#	sleep 10
#done

python article_explorer.py &
