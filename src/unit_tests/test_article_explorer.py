__author__ = 'Roger'

import sys
import os
sys.path.append("..")

import newspaper
from article_explorer import*
import unittest



class TestArticleExplorer(unittest.TestCase):

    def setUp(self):
        sys.stdout = open(os.devnull,"w")

        sys.stout = sys.__stdout__

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_populate_sites_with_no_site(self):

        monitoring_sites = []

        populated_sites = populate_sites(monitoring_sites, True)

        self.assertEqual(len(populated_sites), 0,
                         "The number of populated_sites does not match")



    def test_populate_sites_with_single_site(self):

        monitoring_sites = [["cnn", "http://www.cnn.com/", 2]]

        populated_sites = populate_sites(monitoring_sites, True)

        self.assertEqual(len(populated_sites), 1,
                         "The number of populated_sites does not match")

        self.assertEqual(populated_sites[0][0], "cnn",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[0][1].url, 'http://www.cnn.com/',
                 "The url of the populated_site does not match")

        self.assertEqual(populated_sites[0][2], 2,
                 "The influence of the populated_site does not match")


    def test_populate_sites_with_multiple_sites(self):

        monitoring_sites = [["cnn", "http://www.cnn.com/", 2], ["time", "http://time.com/", 3], ["cbc", "http://www.cbc.ca/",5]]

        populated_sites = populate_sites(monitoring_sites, True)

        self.assertEqual(len(populated_sites), 3,
                         "The number of populated_sites does not match")

        self.assertEqual(populated_sites[0][0], "cnn",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[0][1].url, 'http://www.cnn.com/',
                 "The url of the populated_site does not match")

        self.assertEqual(populated_sites[0][2], 2,
                 "The influence of the populated_site does not match")

        self.assertEqual(populated_sites[1][0], "time",
                 "The name of the populated_site does not match")

        self.assertEqual(populated_sites[1][1].url, 'http://time.com/',
                 "The url of the populated_site does not match")

        self.assertEqual(populated_sites[1][2], 3,
                 "The influence of the populated_site does not match")


        self.assertEqual(populated_sites[2][0], "cbc",
                 "The name of the populated_site does not match")

        self.assertEqual(populated_sites[2][1].url, 'http://www.cbc.ca/',
                 "The url of the populated_site does not match")

        self.assertEqual(populated_sites[2][2], 5,
                 "The influence of the populated_site does not match")



    def test_get_sources_with_no_site(self):

      foreign_sites= []
      html = "<a href='http://www.cnn.com'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URL list is not empty")

      foreign_sites= []
      html = ""
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URL list is not empty")



      foreign_sites= []
      html = "<a href='http://www.cnn.com'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URL list is not empty")


    def test_get_sources_with_single_site(self):

      foreign_sites= ["http://www.cnn.com"]
      html = "<a 'http://www.cnn.com'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URLs dosen't match")


      foreign_sites= ["http://www.cnn.com"]
      html = "<a href='http://www.cnn.com'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, ["http://www.cnn.com"],
                       "The wrong match of ulrs")



      foreign_sites= ["http://www.cnn.com/"]
      html = ""
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URL list is not empty")





    def test_get_sources_with_multi_site(self):

      foreign_sites= ["http://www.cnn.com", "http://www.cbc.ca"]
      html = "<a href='http://www.cnn.com'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, ["http://www.cnn.com"],
                       "The URLs dosen't match")


      foreign_sites= ["http://www.cnn.com", "http://www.cbc.ca"]
      html = "<a href='http://www.cbc.ca'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, ["http://www.cbc.ca"],
                       "The URLs dosen't match")


      foreign_sites= ["http://www.cnn.com", "http://www.cbc.ca"]
      html = "<a href='http://www.cnn.com'></a> <a href='http://www.cbc.ca'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, ["http://www.cnn.com", "http://www.cbc.ca"],
                       "The URLs dosen't match")

      foreign_sites= ["http://www.cnn.com", "http://www.cbc.ca", "http://www.time.com"]
      html = "<a href='http://www.cnn.com'></a> <a href='http://www.cbc.ca'></a>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, ["http://www.cnn.com", "http://www.cbc.ca"],
                       "The URLs dosen't match")


      foreign_sites= ["http://www.cnn.com", "http://www.cbc.ca"]
      html = "<div><p> http://www.cbc.ca </p></div>"
      matched_urls = get_sources(html,foreign_sites)
      self.assertEqual(matched_urls, [],
                       "The URL list is not empty")


    def test_get_keywords_with_no_keyword(self):

      keywords= []
      a = newspaper.article
      a.title = "title"
      a.text = "test get keywords"
      self.assertEqual(get_keywords(a,keywords), [],
                       "This keywords list is not empty")

    def test_get_keywords_with_single_keyword(self):

      keywords= ["keywords"]
      a = newspaper.article
      a.title = "title"
      a.text = "test get keywords"
      self.assertEqual(get_keywords(a,keywords), ["keywords"],
                       "The keywords don't match")

      keywords= ["keywords"]
      a = newspaper.article
      a.title = "title"
      a.text = "test get keyword"
      self.assertEqual(get_keywords(a,keywords), [],
                       "The keywords don't match")

      keywords= ["keywords"]
      a = newspaper.article
      a.title = "keyword"
      a.text = "test"
      self.assertEqual(get_keywords(a,keywords), [],
                       "The keywords don't match")

    def test_get_keywords_with_multi_keyword(self):

      keywords= ["keywords","test"]
      a = newspaper.article
      a.title = "test"
      a.text = "get keywords"
      self.assertEqual(get_keywords(a,keywords), ["keywords", "test"],
                       "The keywords don't match")

      keywords= ["keywords","test"]
      a = newspaper.article
      a.title = "title"
      a.text = "test get keywords"
      self.assertEqual(get_keywords(a,keywords), ["keywords","test"],
                       "The keywords don't match")

      keywords= ["keywords","test"]
      a = newspaper.article
      a.title = "keyword"
      a.text = "tes"
      self.assertEqual(get_keywords(a,keywords), [],
                       "The keywords don't match")



    def test_get_pub_date_with_no_date(self):

      a = newspaper.article
      a.meta_data= {"test":"test"}
      self.assertEqual(get_pub_date(a), None,
                       "The dates don't match")


    def test_get_pub_date_with_with_single_date(self):

      a = newspaper.article
      a.meta_data = {"date":"2014/07/22", "test":"test"}
      self.assertEqual(get_pub_date(a), '2014-07-22T00:00',
                       "The dates don't match")


    def test_get_pub_date_with_with_multi_dates(self):

      a = newspaper.article
      a.meta_data = {"date":"2014/07/22", "date":"2014/07/23"}
      self.assertEqual(get_pub_date(a), '2014-07-23T00:00',
                       "The dates don't match")

if __name__ == '__main__':
    unittest.main(exit=False)
