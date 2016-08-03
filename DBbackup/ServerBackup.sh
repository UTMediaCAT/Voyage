#!/bin/bash

# Please make sure the the password file .pgpass is created for the current user
# https://www.postgresql.org/docs/current/static/libpq-pgpass.html

args=("$@")

database="${args[0]}"
output_dir="${args[1]}"
case "${args[2]}" in
	"add")
		DATE=`date +'%Y-%m-%d_%H:%M:%S'`
		pg_dump  $database > "$output_dir/$database.sql.$DATE";;

	"remove")
		if [ "${args[3]}" == "" ]; then
			echo "Usage: ./ServerBackup.sh [remove] [days]    	Remove the backup file older than [days] days"
		else 


			for old in `ls $output_dir | grep $database`
			do
				old_day=`echo $old  | tail -c 20 | tr _ " "`

				if [ `date -d "$old_day" +%s` -lt `date -d "${args[3]} days ago" +%s` ]; then
					rm -r "$old"
				fi


			done

		fi ;;
	*)
		echo "Usage:"
		echo "./ServerBackup.sh [database_name] [output_dir] [add]         	Backup the database"
		echo "./ServerBackup.sh [database_name] [output_dir] [remove] [days]    	Remove the backup file older than [days] days";;

	



esac 
