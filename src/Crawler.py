import newspaper
from urlparse import urlparse, urljoin, urlunparse
import random
import common
import requests
import re
import logging
import collections
from ExplorerArticle import ExplorerArticle
import urlnorm
'''
An iterator class for iterating over articles in a given site
'''

class Crawler(object):
        def __init__(self, origin_url, filters):
            '''
            (Crawler, str) -> Crawler
            creates a Crawler with a given origin_url
            '''
            self.origin_url = origin_url
            self.filters = filters
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
                    if self.url_in_filter(url, self.filters):
                        logging.info("Matches with filter, skipping the {0}".format(url))
                    try:
                        parsed_url = urlparse(url)
                        parsed_as_list = list(parsed_url)
                        parsed_as_list[5] = ''
                        url = urlunparse(urlnorm.norm_tuple(*parsed_as_list))
                    except ValueError:
                        logging.warn(u"skipping malformed url {0}".format(url))
                        continue
                    if(not parsed_url.netloc.endswith(self.domain)):
                        continue
                    if(url in self.visited_urls):
                        continue
                    self.visit_queue.appendleft(url)
                    self.visited_urls.add(url)
                    logging.info(u"added {0} to the visit queue".format(url))

                self.pages_visited += 1
                return article

        def _should_skip(self):
            n = self.probabilistic_n
            k = self.probabilistic_k
            return False
            return random.random() <= Crawler._s_curve(self.pages_visited/n, k)

        @staticmethod
        def _s_curve(x, k):
            if(x <= 0.5):
                return ((k*(2*x)-(2*x))/(2*k*(2*x)-k-1))*0.5
            else:
                return 0.5*((-k*(2*(x-0.5))-(2*(x-0.5)))/(2*-k*(2*(x-0.5))-(-k)-1))+0.5

        def url_in_filter(self, url, filters):
            '''
            Checks if any of the filters matches the url.
            Filters can be in regex search or normal string comparison.
            '''
            for filt in filters:
                if ((filt[1] and re.search(filt[0], url, re.IGNORECASE)) or
                    (not filt[1] and filt[0] in url)):
                    return True
            return False
