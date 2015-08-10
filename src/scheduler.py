__author__ = 'wangx173'
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


setup()
while True:
    schedule.run_pending()
    time.sleep(1)