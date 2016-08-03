Usage:
./db_backup.sh [User][database_name] [output_dir] [add]                 Backup the database
./db_backup.sh [User][database_name] [output_dir] [remove] [days]       Remove the backup file older than [days] days
For example:
    ./db_backup.sh postgres mediacat ./ add
    ./db_backup.sh postgres mediacat ./ remove 15
Note:

Please make sure the the password file .pgpass is created for the current user
https://www.postgresql.org/docs/current/static/libpq-pgpass.html

If you see:
    FATAL: Peer authentication failed for user "postgres"

    The problem is still your pg_hba.conf file (/etc/postgresql/9.1/main/pg_hba.conf). This line:

    local   all             postgres                                peer
    Should be
    local   all             postgres                                md5

    After altering this file, don't forget to restart your PostgreSQL server:
    sudo service postgresql restart
