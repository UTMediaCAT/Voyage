import newspaper
from urlparse import urlparse, urljoin
import random
import common
import requests
import re
import logging
import collections
from ExplorerArticle import ExplorerArticle
'''
An iterator class for iterating over articles in a given site
'''

class Crawler(object):
        def __init__(self, origin_url):
            '''
            (Crawler, str) -> Crawler
            creates a Crawler with a given origin_url
            '''
            self.origin_url = origin_url
            self.visit_queue = collections.deque([origin_url])
            self.visited_urls = set()
            self.domain = urlparse(origin_url).netloc
            self.pages_visited = 0

            self.probabilistic_n = common.get_config()["crawler"]["n"]
            self.probabilistic_k = common.get_config()["crawler"]["k"]

        def __iter__(self):
            return self

        def next(self):
            '''
            (Crawler) -> newspaper.Article
            returns the next article in the sequence
            '''
            #standard non-recursive tree iteration
            while(True):
                if(len(self.visit_queue) <= 0):
                    raise StopIteration
                current_url = self.visit_queue.pop()

                if(self._should_skip()):
                    logging.info(u"skipping {0} randomly".format(current_url))
                    continue

                logging.info(u"visiting {0}".format(current_url))
                #use newspaper to download and parse the article
                article = ExplorerArticle(current_url)
                article.download()

                #get get urls from the article
                for url in article.get_urls():
                    url = urljoin(current_url, url, False)
                    try:
                        parsed_url = urlparse(url)
                    except ValueError:
                        logging.warn(u"skipping malformed url {0}".format(url))
                        continue
                    if(not parsed_url.netloc.endswith(self.domain)):
                        continue
                    if(url in self.visited_urls):
                        continue
                    self.visit_queue.appendleft(url)
                    logging.info(u"added {0} to the visit queue".format(url))

                self.pages_visited += 1
                self.visited_urls.add(current_url)
                return article

        def _should_skip(self):
            n = self.probabilistic_n
            k = self.probabilistic_k

            return random.random() <= Crawler._s_curve(self.pages_visited/n, k)

        @staticmethod
        def _s_curve(x, k):
            if(x <= 0.5):
                return ((k*(2*x)-(2*x))/(2*k*(2*x)-k-1))*0.5
            else:
                return 0.5*((-k*(2*(x-0.5))-(2*(x-0.5)))/(2*-k*(2*(x-0.5))-(-k)-1))+0.5


