import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)
os.chdir(path)
import warc_creator as wc
import unittest
import time
import shutil

ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter-storm-blasts-" + \
    "eastern-u-s-with-heavy-rain-and-snow-1.2851711"
TWITTER_HTML = "https://twitter.com/wesbos/status/519123918422958081"
WRONG_ARTICLE_HTML = "http://www.cbc.ca/news/world/nor-easter" + \
                     "-storm-blasts-eastern-u-s-with"
WRONG_TWITTER_HTML = "https://twitter.com/wesbos/statu"

WARC_ARTICLE_DIRECTORY = "../warc/article"
WARC_TWITTER_DIRECTORY = "../warc/twitter"

PDF_ARTICLE_DIRECTORY = "../pdf/article"

class TestWarcCreator(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(WARC_ARTICLE_DIRECTORY, ignore_errors=True)
        shutil.rmtree(WARC_TWITTER_DIRECTORY, ignore_errors=True)

    def get_warc_name(self, dir, name_without_ext):
        """
        gets the valid warc filename
        """
        return dir + '/' + name_without_ext.replace('/', '_') + '.warc.gz'

    def get_pdf_name(self, dir, name_without_ext):
        """
        gets the valid pdf filename 
        """
        return dir + '/' + name_without_ext.replace('/', '_') + '.pdf'

    def assertWarcFile(self, dir, name_without_ext):
        """
        assert the given warc file exists
        """
        path = self.get_warc_name(dir, name_without_ext)
        self.assertTrue(os.path.isfile(path))

    def assertPdfFile(self, dir, name_without_ext):
        """
        assert the given pdf file exists
        """
        path = self.get_pdf_name(dir, name_without_ext)
        self.assertTrue(os.path.isfile(path))

    def test_create_article_warc(self):
        """
        create a real article url warc should work
        """
        filename = ARTICLE_HTML.replace('/', '_')
        wc.create_article_warc(ARTICLE_HTML, filename).wait()
        self.assertWarcFile(WARC_ARTICLE_DIRECTORY, filename)

    def test_create_twitter_warc(self):
        """
        create a real twitter url warc should work
        """
        wc.create_twitter_warc(TWITTER_HTML).wait()
        self.assertWarcFile(WARC_TWITTER_DIRECTORY, TWITTER_HTML);

    def test_create_wrong_url_article_warc(self):
        """
        crawling a wrong url article should be going to success because there
        is 404 page
        """
        filename = WRONG_ARTICLE_HTML.replace('/', '_')
        wc.create_article_warc(WRONG_ARTICLE_HTML, filename).wait()
        self.assertWarcFile(WARC_ARTICLE_DIRECTORY, filename)

    def test_create_wrong_url_twitter_warc(self):
        """
        crawling a wrong twitter article should be going to success because
        there is 404 page
        """
        wc.create_twitter_warc(WRONG_TWITTER_HTML).wait()
        self.assertWarcFile(WARC_TWITTER_DIRECTORY, WRONG_TWITTER_HTML)

    def test_create_exist_twitter_warc(self):
        """
        crawling a exist twitter warc will replace new
        """
        warc_name = self.get_warc_name(WARC_TWITTER_DIRECTORY, TWITTER_HTML)
        
        wc.create_twitter_warc(TWITTER_HTML).wait()
        mtime1 = os.path.getmtime(warc_name)
        
        wc.create_twitter_warc(TWITTER_HTML).wait()
        mtime2 = os.path.getmtime(warc_name)
        
        self.assertGreater(mtime2, mtime1)

    def test_create_exist_article_warc(self):
        """
        crawling a exist article warc will replace new
        """
        filename = ARTICLE_HTML.replace('/', '_')
        warc_name = self.get_warc_name(WARC_ARTICLE_DIRECTORY, ARTICLE_HTML)

        wc.create_article_warc(ARTICLE_HTML, filename).wait()
        mtime1 = os.path.getmtime(warc_name)

        wc.create_article_warc(ARTICLE_HTML, filename).wait()
        mtime2 = os.path.getmtime(warc_name)

        self.assertGreater(mtime2, mtime1)

    def test_create_article_pdf(self):
        """
        create a real article pdf should work
        """
        filename = ARTICLE_HTML.replace('/', '_')
        pdf_name = self.get_pdf_name(PDF_ARTICLE_DIRECTORY, ARTICLE_HTML)

        wc.create_article_pdf(ARTICLE_HTML, filename).wait()
        self.assertPdfFile(PDF_ARTICLE_DIRECTORY, filename)

if __name__ == "__main__":
    unittest.main()
