__author__ = 'Roger'

import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)
os.chdir(path)
from article_explorer import*
from datetime import datetime


import newspaper

import unittest


class ArticleTestBase(unittest.TestCase):
    SENTENCE = "I can eat glass, it does not hurt me."

    def setUp(self):
        sys.stdout = open(os.devnull, "w")

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def from_html(self, html):
        a = ExplorerArticle('')
        a.html = '<!DOCTYPE html>' + html
        return a

class GetPubDateTest(ArticleTestBase):
    def test_no_date(self):
        a = self.from_html('abc')
        a.newspaper_parse()
        self.assertEqual(get_pub_date(a), None,
                         "The dates don't match")

    def test_single_date(self):
        a = self.from_html(
            '<meta property="article:published_time" content="2013-12-30T21:42:01+00:00"/>')
        a.newspaper_parse()
        self.assertEqual(
            get_pub_date(a).date(),
            datetime.strptime(
                '2013-12-30',
                "%Y-%m-%d").date(),
            "The dates don't match")

    def test_multi_dates(self):
        a = self.from_html('<meta property="article:modified_time" content="2014/07/22"/>'
                           '<meta property="article:published_time" content="2014/07/23"')
        a.newspaper_parse()
        self.assertEqual(
            get_pub_date(a).date(),
            datetime.strptime(
                '2014-07-23',
                "%Y-%m-%d").date(),
            "The dates don't match")


class GetSourcesSitesTest(ArticleTestBase):

    def assertEmpty(self, urls):
        self.assertEqual(urls, [[], []],
                         "The URL list is not empty: " + str(urls))

    def assertResult(self, actual, matched=[], unmatched=[]):
        self.assertEqual(actual,
                         [matched, unmatched],
                         "The URLs do not match, got: " + str(actual))

    def test_no_site(self):

        site = ["http://www.cnn.com", "cnn.com", "link"]

        foreign_sites = []

        a = self.from_html(
            self.SENTENCE + "<a href='http://www.cnn.com'>link</a>")
        matched_unmatched = get_sources_sites(a, [])
        self.assertResult(matched_unmatched, unmatched=[site])

        a = self.from_html(self.SENTENCE)
        matched_unmatched = get_sources_sites(a, [])
        self.assertEmpty(matched_unmatched)

        a = self.from_html(
            self.SENTENCE + "<a href='http://www.cnn.com'>link</a>")
        matched_unmatched = get_sources_sites(a, [])
        self.assertResult(matched_unmatched, unmatched=[site])

    def test_single_site(self):

        site = ["http://www.cnn.com", "cnn.com", "link"]

        foreign_sites = ["http://www.cnn.com"]
        a = self.from_html(self.SENTENCE + "<a 'http://www.cnn.com'>link</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertEmpty(matched_unmatched)

        foreign_sites = ["http://www.cnn.com"]
        a = self.from_html(
            self.SENTENCE + "<a href='http://www.cnn.com'>link</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertResult(matched_unmatched, matched=[site])

        foreign_sites = ["http://www.cnn.com/"]
        a = self.from_html(self.SENTENCE)
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertEmpty(matched_unmatched)

    def test_multi_site(self):
        foreign_sites = ["http://www.cnn.com", "http://www.cbc.ca"]
        a = self.from_html(
            self.SENTENCE + "<a href='http://www.cnn.com/article'>link</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertResult(matched_unmatched,
                          matched=[['http://www.cnn.com/article', 'cnn.com', 'link']])

        foreign_sites = ["http://www.cnn.com", "http://www.cbc.ca"]
        a = self.from_html(
            self.SENTENCE + "<a href='http://www.cbc.ca/news'>link</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertResult(matched_unmatched,
                          matched=[['http://www.cbc.ca/news', 'cbc.ca', 'link']])

        foreign_sites = ["http://www.cnn.com", "http://www.cbc.ca"]
        a = self.from_html(self.SENTENCE +
                           "<a href='http://www.cnn.com'>link1</a> <a href='http://www.cbc.ca'>link2</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertResult(matched_unmatched,
                          matched=[
                              ['http://www.cnn.com', 'cnn.com', 'link1'],
                              ['http://www.cbc.ca', 'cbc.ca', 'link2']
                          ])

        foreign_sites = [
            "http://www.cnn.com",
            "http://www.cbc.ca",
            "http://www.time.com"]
        a = self.from_html(self.SENTENCE +
                           "<a href='http://www.cnn.com/news'>link1</a> <a href='http://www.cbc.ca/news'>link2</a>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertResult(matched_unmatched,
                          matched=[
                              ['http://www.cnn.com/news', 'cnn.com', 'link1'],
                              ['http://www.cbc.ca/news', 'cbc.ca', 'link2']
                          ])

        foreign_sites = ["http://www.cnn.com", "http://www.cbc.ca"]
        a = self.from_html(self.SENTENCE + "<div><p> http://www.cbc.ca </p></div>")
        matched_unmatched = get_sources_sites(a, foreign_sites)
        self.assertEmpty(matched_unmatched)


class TestArticleExplorer(unittest.TestCase):
    def setUp(self):
        sys.stdout = open(os.devnull, "w")

        sys.stout = sys.__stdout__

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_populate_sites_with_no_site(self):

        monitoring_sites = []

        populated_sites = populate_sites(monitoring_sites)

        self.assertEqual(len(populated_sites), 0,
                         "The number of populated_sites does not match")

    def test_populate_sites_with_single_site(self):

        monitoring_sites = [["cnn", "http://www.cnn.com/", 2]]

        populated_sites = populate_sites(monitoring_sites)

        self.assertEqual(len(populated_sites), 1,
                         "The number of populated_sites does not match")

        self.assertEqual(populated_sites[0][0], "cnn",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[0][1].url, 'http://www.cnn.com/',
                         "The url of the populated_site does not match")

    def test_populate_sites_with_multiple_sites(self):

        monitoring_sites = [["cnn",
                             "http://www.cnn.com/",
                             2],
                            ["time",
                             "http://time.com/",
                             3],
                            ["cbc",
                             "http://www.cbc.ca/",
                             5]]

        populated_sites = populate_sites(monitoring_sites)

        self.assertEqual(len(populated_sites), 3,
                         "The number of populated_sites does not match")

        self.assertEqual(populated_sites[0][0], "cnn",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[0][1].url, 'http://www.cnn.com/',
                         "The url of the populated_site does not match")

        self.assertEqual(populated_sites[1][0], "time",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[1][1].url, 'http://time.com/',
                         "The url of the populated_site does not match")

        self.assertEqual(populated_sites[2][0], "cbc",
                         "The name of the populated_site does not match")

        self.assertEqual(populated_sites[2][1].url, 'http://www.cbc.ca/',
                         "The url of the populated_site does not match")

    def test_get_keywords_with_no_keyword(self):

        keywords = []
        a = ExplorerArticle('')
        a.newspaper_article.title = "title"
        a.newspaper_article.text = "test get keywords"
        self.assertEqual(get_keywords(a, keywords), [],
                         "This keywords list is not empty")

    def test_get_keywords_with_single_keyword(self):

        keywords = ["keywords"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "title"
        a.newspaper_article.text = "test get keywords"
        self.assertEqual(get_keywords(a, keywords), ["keywords"],
                         "The keywords don't match")

        keywords = ["keywords"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "title"
        a.newspaper_article.text = "test get keyword"
        self.assertEqual(get_keywords(a, keywords), [],
                         "The keywords don't match")

        keywords = ["keywords"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "keyword"
        a.newspaper_article.text = "test"
        self.assertEqual(get_keywords(a, keywords), [],
                         "The keywords don't match")

    def test_get_keywords_with_multi_keyword(self):

        keywords = ["keywords", "test"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "test"
        a.newspaper_article.text = "get keywords"
        self.assertEqual(get_keywords(a, keywords), ["keywords", "test"],
                         "The keywords don't match")

        keywords = ["keywords", "test"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "title"
        a.newspaper_article.text = "test get keywords"
        self.assertEqual(get_keywords(a, keywords), ["keywords", "test"],
                         "The keywords don't match")

        keywords = ["keywords", "test"]
        a = ExplorerArticle('')
        a.newspaper_article.title = "keyword"
        a.newspaper_article.text = "tes"
        self.assertEqual(get_keywords(a, keywords), [],
                         "The keywords don't match")

if __name__ == '__main__':
    unittest.main(exit=False)
