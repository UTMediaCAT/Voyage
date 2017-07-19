'''
This is an in-process scheduler for periodic jobs that uses the
builder pattern for configuration. Schedule lets you run Python
functions (or any other callable) periodically at pre-determined intervals.
we use this to cache statistics data and back up database periodically
'''


__author__ = 'wangx173'
import sys
import os
# Add Django directories in the Python paths for django shell to work
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'

django.setup()
import schedule
import time
import subprocess



def backup_db_add ():
    '''
    Run Server backup bash script to backup database
    '''
    subprocess.call(["./ServerBackup.sh","add"])

def backup_db_remove ():
    '''
    Run Server backup bash script to remove 10 days old databse
    '''
    subprocess.call(["./ServerBackup.sh","remove","10"])

def  setup():
    '''
    Configure schedule
    '''
    # backup data base everyday
    schedule.every(1).days.do(backup_db_add)
    schedule.every(1).days.do(backup_db_remove)



if __name__ == "__main__":
    # setup django and run schedule
    setup()
    while True:
        schedule.run_pending()
        time.sleep(1) #avoid busy  looping
