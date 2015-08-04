__author__ = 'wangx173'
import schedule
import time
import Caching


def  setup():

    schedule.every(10).minutes.do(Caching.setArticleCachedData)
    schedule.every(10).minutes.do(Caching.setTweetCachedData)



setup()
while True:
    schedule.run_pending()
    time.sleep(1)