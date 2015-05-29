#!/bin/bash



args=("$@")

BASEDIR=$(dirname $0)
cd $BASEDIR
cd ../Frontend
case "${args[0]}" in 
	"add")
		DATE=`date +%Y-%m-%d:%H:%M:%S`
		sqlite3 db.sqlite3 ".backup DatabaseBackup/bk_$DATE.sqlite3";;

	"remove")
		if [ "${args[1]}" == "" ]; then
			echo "Usage: ./ServerBackup.sh [remove] [days]    	Remove the backup file older than [days] days"
		else 
			find ./DatabaseBackup -mtime +"${args[1]}"  -type f -delete
		fi ;;
	*)
		echo "Usage:"
		echo "./ServerBackup.sh [ add ]         	Backup the database"
		echo "./ServerBackup.sh [remove] [days]    	Remove the backup file older than [days] days";;

	



esac 