#!/bin/bash



args=("$@")

BASEDIR=$(dirname $0)
cd $BASEDIR
cd ../Frontend
case "${args[0]}" in 
	"add")
		DATE=`date +'%Y-%m-%d_%H:%M:%S'`
		sqlite3 db.sqlite3 ".backup DBbackup/db.sqlite3.$DATE";;

	"remove")
		if [ "${args[1]}" == "" ]; then
			echo "Usage: ./ServerBackup.sh [remove] [days]    	Remove the backup file older than [days] days"
		else 


			for old in `ls ./DBbackup`
			do
				old_day=`echo $old  | cut -c 12-30 | tr _ " "`

				if [`date -d "$old_day " +%s` -lt `date -d "${args[1]} days ago"  +%s` ]; then 
					rm -r "./DBbackup/$old"
				fi


			done

		fi ;;
	*)
		echo "Usage:"
		echo "./ServerBackup.sh [ add ]         	Backup the database"
		echo "./ServerBackup.sh [remove] [days]    	Remove the backup file older than [days] days";;

	



esac 