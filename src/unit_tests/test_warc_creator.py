import sys
sys.path.append("..")
import warc_creator as wc
import os
os.chdir(os.getcwd())
os.chdir("../..")
import unittest
import time


ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter-storm-blasts-eastern-u-s-with-heavy-rain-and-snow-1.2851711"
TWITTER_HTML = "https://twitter.com/wesbos/status/519123918422958081"
WRONG_ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter-storm-blasts-eastern-u-s-with"
WRONG_TWITTER_HTML = "https://twitter.com/wesbos/statu"
WARC_ARTICLE_DIRECTORY = "warc/article"
WARC_TWITTER_DIRECTORY = "warc/twitter"


class TestWarcCreator(unittest.TestCase):
    def setUp(self):     
        os.chdir("./src")
        
        
    def test_create_article_warc(self):
        """
        create a real article url warc should work
        """
        try:
            os.chdir("..")
            os.remove(WARC_ARTICLE_DIRECTORY+"/http:__www.cbc.ca_news_world_nor-easter-storm-blasts-eastern-u-s-with-heavy-rain-and-snow-1.2851711.warc.gz")
        except OSError:
            pass      
        self.setUp()
        wc.create_article_warc(ARTICLE_HTML)
        os.chdir("..")
        time.sleep(1)
        self.assertTrue(os.path.isfile(WARC_ARTICLE_DIRECTORY+"/http:__www.cbc.ca_news_world_nor-easter-storm-blasts-eastern-u-s-with-heavy-rain-and-snow-1.2851711.warc.gz") )
        
    def test_create_twitter_warc(self):
        """
        create a real twitter url warc should work
        """
        try:
            os.chdir("..")
            os.remove(WARC_TWITTER_DIRECTORY+"/https:__twitter.com_wesbos_status_519123918422958081.warc.gz")
        except OSError:
            pass   
        self.setUp()
        wc.create_twitter_warc(TWITTER_HTML)
        os.chdir("..")
        time.sleep(1)
        self.assertTrue(os.path.isfile(WARC_TWITTER_DIRECTORY+"/https:__twitter.com_wesbos_status_519123918422958081.warc.gz") ) 
        
        
    def test_create_wrong_url_article_warc(self):
        """
        crawling a wrong url article should be going to success because there is 
        404 page
        """        
        try:
            os.chdir("..")
            os.remove(WARC_ARTICLE_DIRECTORY+"/http:__www.cbc.ca_news_world_nor-easter-storm-blasts-eastern-u-s-with.warc.gz")
        except OSError:
            pass      
        self.setUp()
        wc.create_article_warc(WRONG_ARTICLE_HTML)
        os.chdir("..")
        time.sleep(1)
        self.assertTrue(os.path.isfile(WARC_ARTICLE_DIRECTORY+"/http:__www.cbc.ca_news_world_nor-easter-storm-blasts-eastern-u-s-with.warc.gz") )  
    
    def test_create_wrong_url_twitter_warc(self):
        """
        crawling a wrong url twitter should be not going to warc because there is 
        such twitter response to crawl
        """
        wc.create_twitter_warc(TWITTER_HTML)
        os.chdir("..")
        self.assertTrue(not os.path.isfile(WARC_TWITTER_DIRECTORY+"/https:__twitter.com_wesbos_statu.warc.gz") )    
        


if __name__=="__main__":
    unittest.main()
    