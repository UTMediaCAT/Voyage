__author__ = 'wangx173'
import sys
import os
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'

django.setup()
import schedule
import time
import Caching
import subprocess



def backup_db_add ():
    subprocess.call(["./ServerBackup.sh","add"])

def backup_db_remove ():
    subprocess.call(["./ServerBackup.sh","remove","10"])

def  setup():
    schedule.every(10).minutes.do(Caching.setArticleCachedData)
    schedule.every(10).minutes.do(Caching.setTweetCachedData)
    schedule.every(1).days.do(backup_db_add)
    schedule.every(1).days.do(backup_db_remove)



if __name__ == "__main__":

    setup()
    while True:
        schedule.run_pending()
        time.sleep(1)
