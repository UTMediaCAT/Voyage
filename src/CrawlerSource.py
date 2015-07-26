import newspaper
from urlparse import urlparse, urljoin
import random
import common
import requests
import re
import logging

'''
An iterator class for iterating over articles in a given site
'''

class CrawlerSource(object):
        def __init__(self, origin_url):
            '''
            (CrawlerSource, str) -> CrawlerSource
            creates a CrawlerSource with a given origin_url
            '''
            self.origin_url = origin_url
            self.visit_queue = [origin_url]
            self.visited_urls = []
            self.domain = urlparse(origin_url).netloc
            self.pages_visited = 0

            self.probabilistic_n = common.get_config()["crawler"]["n"]
            self.probabilistic_k = common.get_config()["crawler"]["k"]

        def __iter__(self):
            return self

        def next(self):
            '''
            (CrawlerSource) -> newspaper.Article
            returns the next article in the sequence
            '''
            #standard non-recursive tree iteration
            while(True):
                if(len(self.visit_queue) <= 0):
                    raise StopIteration
                url = self.visit_queue.pop()
                if(url in self.visited_urls):#don't visit links that we've seen before
                    logging.info("skipping {0} because it was already visited".format(url))
                    continue

                if(self._should_skip()):
                    logging.info("skipping {0} randomly".format(url))

                if(not CrawlerSource._is_html(url)):
                    logging.info("skipping {0} because the content-type isn't html".format(url))

                logging.info("visiting {0}".format(url))
                #use newspaper to download and parse the article
                article = newspaper.Article(url)
                article.config.fetch_images = False
                article.download()
                try:
                    article.parse()
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    continue
                #get get urls from the article
                article_urls = article.extractor.get_urls(article.doc)
                logging.info("got {0} urls from document".format(len(article_urls)))
                #add them to the visit queue
                for u in article_urls:
                    u = urljoin(url, u, False)#fix for relative urls
                    parsed_url = urlparse(url)
                    if(self.domain.endswith(parsed_url.netloc)):
                        self.visit_queue.insert(0, u)
                        logging.info("added {0} to the visit queue".format(u))

                self.pages_visited += 1
                self.visited_urls.append(url)
                return article

        def _should_skip(self):
            n = self.probabilistic_n
            k = self.probabilistic_k
            return random.random() < CrawlerSource._s_curve(self.pages_visited/n, k)

        @staticmethod
        def _is_html(url):
            try:
                response = requests.head(url, allow_redirects=True)
                r = re.compile("(text/html|application/xhtml\+xml|application/xml) *(; .*)?")
                if(r.match(response.headers["content-type"])):
                    return True
                logging.debug("not a html: {0}".format(response.headers["content-type"]))
            except requests.RequestException:
                pass
            except KeyError:
                return True
            return False

        @staticmethod
        def _s_curve(x, k):
            if(x <= 0.5):
                return ((k*(2*x)-(2*x))/(2*k*(2*x)-k-1))*0.5
            else:
                return 0.5*((-k*(2*(x-0.5))-(2*(x-0.5)))/(2*-k*(2*(x-0.5))-(-k)-1))+0.5

