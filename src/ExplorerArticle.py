import newspaper
import requests
import logging
from readability import Document
import re
import lxml.html
from bs4 import UnicodeDammit

class ExplorerArticle(object):#derive from object for getters/setters
    def __init__(self, url):
        self.url = url
        self.canonical_url = url
        self.newspaper_article = newspaper.Article(url)
        self.newspaper_article.config.fetch_images = False
        self.is_downloaded = False
        self._readability_title = None
        self._readability_text = None

    def download(self):
        '''
        modified from https://github.com/codelucas/newspaper/blob/master/newspaper/network.py
        '''
        if(self.is_downloaded):
            return True

        FAIL_ENCODING = 'ISO-8859-1'
        useragent = self.newspaper_article.config.browser_user_agent
        timeout = self.newspaper_article.config.request_timeout

        try:
            html = None
            response = requests.get(url=self.url)#TODO: add back get_request_kwargs functionality present in newspaper impl
            if(response.status_code >= 400):
                logging.warn(u"encountered status code {0} while getting {1}".format(response.status_code, self.url))
                return False

            if(not re.search("(text/html|application/xhtml\+xml) *(; .*)?", response.headers["content-type"])):
                logging.debug(u"not a html: {0}".format(response.headers["content-type"]))
                return False

            self.canonical_url = response.url

            if response.encoding != FAIL_ENCODING:
                html = response.text
            else:
                html = response.content
            if not html:
                return False

            converted = UnicodeDammit(html, is_html=True)
            if not converted.unicode_markup:
                logging.warn("Failed to detect encoding of downloaded article, tried: " + ", ".join(converted.tried_encodings))
                return False
            self.html = converted.unicode_markup
            self.is_downloaded = True
        except Exception as e:
            logging.warn('%s on %s' % (e, self.url))
            return False
        return True

    def preliminary_parse(self):
        if(not self.is_downloaded):
            raise Exception("not downloaded")
        try:
            d = Document(self.html)
            self._readability_title = d.short_title()
            self._readability_text = d.summary()
            logging.debug(u"readability title: {0}".format(repr(self._readability_title)))
            logging.debug(u"readability text: {0}".format(repr(self._readability_text)))
            if(self._readability_title and self._readability_text):
                return
        except Exception as e:
            logging.warning("error while doing readability parse: {0}".format(str(e)))

        logging.debug("falling back to newspaper parse")
        self.newspaper_article.parse()
        logging.debug(u"newspaper title: {0}".format(repr(self._newspaper_title)))
        logging.debug(u"newspaper text: {0}".format(repr(self._newspaper_text)))

    def newspaper_parse(self):
        return self.newspaper_article.parse()

    @property
    def html(self):
        return self.newspaper_article.html

    @html.setter
    def html(self, value):
        self.newspaper_article.download(value)

    @property
    def authors(self):
        return self.newspaper_article.authors

    @property
    def _newspaper_title(self):
        return self.newspaper_article.title

    @property
    def _newspaper_text(self):
        return self.newspaper_article.text

    @property
    def title(self):
        return self._readability_title or self._newspaper_title

    @property
    def text(self):
        return self._readability_text or self._newspaper_text


    def get_urls(self, article_text_links_only=False):
        result = []
        try:
            if(article_text_links_only):
                if(self._readability_text):
                    lxml_tree = lxml.html.fromstring(self._readability_text)
                else:
                    if(not self.newspaper_article.is_parsed):
                        self.newspaper_article.parse()
                        if(self.newspaper_article.clean_top_node):
                            lxml_tree = self.newspaper_article.clean_top_node
                        else:
                            logging.warning("no links could be obtained because both methods of obtaining a cleaned document failed")
                            return []
            else:
                lxml_tree = lxml.html.fromstring(self.html)
        except lxml.etree.Error as e:
            logging.warning("error while getting links from article: {0}".format(str(e)))
            return []
        for e in lxml_tree.cssselect("a"):
            href = e.get("href")
            if(href):
                result.append(href)
        return result