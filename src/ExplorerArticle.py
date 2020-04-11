import newspaper
import requests
import logging
from readability import Document
import re
import lxml.html
from bs4 import UnicodeDammit
import collections
#import urlnorm
import urltools
from urllib.parse import urlparse, urljoin, urlunparse
import subprocess as sp
import json
import time
import asyncio
import os

# For absolute download timeout
import eventlet
eventlet.monkey_patch(socket=True)

Link = collections.namedtuple("Link", ["href", "text"])

import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class ExplorerArticle(object):#derive from object for getters/setters
    def __init__(self, object):
        if (isinstance(object, tuple)):
            url = object[0]
        else:
            url = object
        logging.info("url is: {0}".format(url))
        self.url = url
        self.canonical_url = url
        self.newspaper_article = newspaper.Article(url)
        self.newspaper_article.config.fetch_images = False
        self.is_downloaded = False
        self.is_parsed = False
        self._readability_title = None
        self._readability_text = None
        self.stdout = ""

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
            with eventlet.Timeout(15):
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                response = requests.get(url=self.url, timeout=15, headers=headers)#TODO: add back get_request_kwargs functionality present in newspaper impl
            if(response.status_code >= 400):
                logging.warn("encountered status code {0} while getting {1}".format(response.status_code, self.url))
                return False

            if(not re.search("(text/html|application/xhtml\+xml) *(; .*)?", response.headers["content-type"])):
                logging.debug("not a html: {0}".format(response.headers["content-type"]))
                return False

            try:
                parsed_url = urlparse(response.url)
                parsed_as_list = list(parsed_url)
                parsed_as_list[5] = ''
                self.canonical_url = parsed_url.geturl()
            except Exception as e:
                logging.info("skipping malformed url {0}. Error: {1}".format(response.url, str(e)))
                return False

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
        except eventlet.Timeout as t:
            logging.warn('Timeout on %s' % (self.url))
            return False
        return True

    def preliminary_parse(self):
        if(not self.is_downloaded):
            raise Exception("not downloaded")
        try:
            d = Document(self.html)
            self._readability_title = d.short_title()
            self._readability_text = d.summary()
            logging.debug("readability title: {0}".format(repr(self._readability_title)))
            logging.debug("readability text: {0}".format(repr(self._readability_text)))
            if(self._readability_title and self._readability_text):
                self.is_parsed = True
                return True
        except Exception as e:
            logging.warning("error while doing readability parse: {0}".format(str(e)))
            return False

        logging.debug("falling back to newspaper parse")
        self.newspaper_article.parse()
        logging.debug("newspaper title: {0}".format(repr(self._newspaper_title)))
        logging.debug("newspaper text: {0}".format(repr(self._newspaper_text)))
        self.is_parsed = True
        return True

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
    def language(self):
        return self.newspaper_article.meta_lang
    
    def get_text(self, strip_html=False):
        if(strip_html):
            if(self._newspaper_text):
                return self._newspaper_text
            else:
                try:
                    return lxml.html.fromstring(self._readability_text).text_content()
                except lxml.etree.Error as e:
                    return ""
        else:
            return self._newspaper_text or self._readability_text

    text = property(get_text)

    def get_links(self, article_text_links_only=False):
        result = []
        # logging.info("AAAAAAAAAAAAA\n")

        # logging.info(self.html)

        # logging.info("AAAAAAAAAAAAA\n")

        result_file_name = randomString(5) + '.txt'
        try:
            # self.html = PyppeteerCrawl.run_crawl(self.url)
            
            # outputs = sp.check_output(["node", "crawl.js", "-l", self.url])
            # print(output)

            
            # loop = asyncio.get_event_loop()

            # tasks = [
            #     asyncio.ensure_future(self.do_subprocess()),
            #     asyncio.ensure_future(self.sleep_report(5)),
            # ]

            # loop.run_until_complete(asyncio.gather(*tasks))
            # loop.close()

            # res = ""
            # for line in self.stdout:
            #     line = line.decode("utf-8")
            #     res = line

            # print(res)
            # jsonObj = json.loads(res)
            # for x in jsonObj:
            #     # print(x)
            #     for ele in jsonObj[x]:
            #         # print(ele)
            #         href = ele[0]
            #         href = str(href)
            #         # print(ele[1])
            #         result.append(Link(href=href, text=ele[1]))
            # print(result)
            
            # --------------- 
            # child = sp.Popen(["node", "../javascript_crawler_script/crawl.js", "-l", self.url], stdout=sp.PIPE)
            child = sp.Popen(["node", "./js_crawler/main.js", "-l", self.url, "-f", result_file_name], stdout=sp.PIPE)
            res = []
            # print("child.wait: " + str(child.wait()))
            while child.poll() is None:
                # print('Still sleeping ' + self.url)
                time.sleep(1)

            try:
                with open("./js_crawler/result_file/" + result_file_name, encoding='utf-8') as result_file:
                    logging.info("reading")
                    json_data = json.loads(result_file.read())
                    res = json_data
                    logging.info("reading done")
            except Exception as e:
                logging.exception("cannot read: " + str(e))



            # lines = result_file.readlines()
            # if len(lines) > 1:
            #     for line in lines:
            #         print(line.strip())
            # else:
            
            # res = ""
            # for line in child.stdout:
            #     line = line.decode("utf-8")
            #     res = line
            #     # print(self.url+ " " + res)
            #     if (res[0] == '{'):
            #         print(self.url+ " " + res)
            #         break

            logging.info("LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            logging.info("res from main.js of {0}: {1}".format(self.url, res))
            # print(res)
            
            # jsonObj = json.loads(res)
            # for x in jsonObj:
            for x in res:
                # print(x)
                for ele in res[x]:
                    # logging.info(ele)
                    href = ele[0]
                    href = str(href)
                    # print(ele[1])
                    result.append(Link(href=href, text=ele[1]))
                    
            # log for checking the list of all url and its title
            # logging.info("result of {0}: {1}".format(self.url, result))

            # remove the result_file after read successfully
            if os.path.exists("./js_crawler/result_file/" + result_file_name):
                os.remove("./js_crawler/result_file/" + result_file_name)
            else:
                logging.warning("The file "+ result_file_name + " does not exist")


            # result = []
            # for output in outputs:
            #     a = Link(href=output[0], text=output[1])
            #     result.append(a)

            # logging.info("-----========================================================")
            # logging.info("url: %s", self.url)
            # logging.info("%s", self.html)
            # if(article_text_links_only):
            #     if(self._readability_text):
            #         lxml_tree = lxml.html.fromstring(self._readability_text)
            #     else:
            #         if(not self.newspaper_article.is_parsed):
            #             self.newspaper_article.parse()
            #             if(self.newspaper_article.clean_top_node):
            #                 lxml_tree = self.newspaper_article.clean_top_node
            #             else:
            #                 logging.warning("no links could be obtained because both methods of obtaining a cleaned document failed")
            #                 return []
            # else:
            #     lxml_tree = lxml.html.fromstring(self.html)
        except Exception as e:
            logging.warning("error while converting links {0} from article--------: {1}".format(self.url, e))
            logging.warning("%s", result)
            return []
        except IOError:
            logging.warning("File " + result_file_name + "not accessible")
            return []
        # for e in lxml_tree.cssselect("a"):
        #     href = e.get("href")
        #     text = e.text_content()
        #     if(href):
        #         result.append(Link(href=href, text=text))
        return result

    def evaluate_css_selectors(self, selectors):
        lxml_tree = lxml.html.fromstring(self.html)
        for select in selectors:
            try:
                result = lxml_tree.cssselect(select.pattern)
                if(select.regex):
                    result = re.search(select.regex, result).groups()[-1]
            except lxml.cssselect.SelectorSyntaxError:
                logging.error("invaild css selector \"{0}\"".format(select.pattern))
                continue
            if(len(result) > 0):
                if(len(result) > 1):
                    logging.error("css selector \"{0}\" matched multiple elements. selecting the first one!".format(select.pattern))
                return result[0].text_content()
        return None
