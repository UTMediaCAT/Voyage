import sys
sys.path.append("..")
import os
os.chdir(os.getcwd())
os.chdir("../..")
import unittest
import warc_creator as wc

ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter-storm-blasts-eastern-u-s-with-heavy-rain-and-snow-1.2851711"
TWITTER_HTML = "https://twitter.com/wesbos/status/519123918422958081"
WRONG_ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter-storm-blasts-eastern-u-s-with"
WRONG_TWITTER_HTML = "https://twitter.com/wesbos/statu"
WARC_ARTICLE_DIRECTORY = "warc/article"
WARC_TWITTER-DIRECTORY = "warc/twitter"


class TestWarcCreator(unittest.TestCase):
    def test_create_article_warc(self):
        wc.create_article_warc(ARTICLE_HTML)
        self.assertTrue(os.path.isfile(WARC_ARTICLE_DIRECTORY+"/http:\\\\www.cbc.ca\\news\\world\\nor-easter-storm-blasts-eastern-u-s-with-heavy-rain-and-snow-1.2851711.warc.gz") )
        


if __name__=="__main__":
    unittest.main()
    #print(os.path.isfile("warc/article/http:\\\\ac360.blogs.cnn.com\\2012\\06\\18\\tonight-on-ac360-child-sex-abuse-scandal\\.warc.gz") )
    
    #print( os.getcwd())