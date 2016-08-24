from urlparse import urlparse, urljoin, urlunparse
import random
import common
import re
import logging
from ExplorerArticle import ExplorerArticle
import urlnorm
import psycopg2
import time
'''
An iterator class for iterating over articles in a given site
'''

class Crawler(object):
    def __init__(self, site, transactions_file):
        '''
        (Crawler, str) -> Crawler
        creates a Crawler with a given origin_url
        '''
        self.site = site
        self.filters = []
        self.domain = urlparse(site.url).netloc
        self.pages_visited = 0

        self.probabilistic_n = common.get_config()["crawler"]["n"]
        self.probabilistic_k = common.get_config()["crawler"]["k"]

        self.db = psycopg2.connect(host='localhost',
                                   database="crawler",
                                   user="postgres",
                                   password="password")
                                   
        self.cursor = self.db.cursor()
        self.already_added_urls = set()
        self.visited_table = "visited_" + str(site.id)
        self.tovisit_table = "tovisit_" + str(site.id)

        self.cursor.execute("DROP TABLE IF EXISTS " + self.visited_table)
        self.cursor.execute("CREATE TABLE " + self.visited_table + " (url VARCHAR(1024) PRIMARY KEY)")
        self.cursor.execute("DROP TABLE IF EXISTS " + self.tovisit_table)
        self.cursor.execute(u"CREATE TABLE " + self.tovisit_table + " (id SERIAL PRIMARY KEY, url VARCHAR(1024))")

        self.cursor.execute(u"INSERT INTO " + self.visited_table + " VALUES (%s)", (site.url,))
        self.cursor.execute(u"INSERT INTO " + self.tovisit_table + " VALUES (DEFAULT, %s)", (site.url,))
        self.transactions_file = transactions_file

        self.db.commit()

    def __iter__(self):
        return self

    def next(self):
        '''
        (Crawler) -> newspaper.Article
        returns the next article in the sequence
        '''

        #standard non-recursive tree iteration
        try:
            while(True):
                tovisit_pop_start = time.time()
                self.cursor.execute("SELECT * FROM " + self.tovisit_table + " ORDER BY id LIMIT 1")
                row = self.cursor.fetchone()
                if(row):
                    row_id = row[0]
                    current_url = row[1]
                    self.transactions_file.write("1" + current_url)
                    self.cursor.execute("DELETE FROM " + self.tovisit_table + " WHERE id=%s", (row_id,))
                    self.db.commit()
                else:
                    raise StopIteration
                tovisit_pop_total = time.time() - tovisit_pop_start

                if(self._should_skip()):
                    logging.info(u"skipping {0} randomly".format(current_url))
                    continue

                logging.info(u"visiting {0}".format(current_url))
                #use newspaper to download and parse the article

                article_download_start = time.time()
                article = ExplorerArticle(current_url)
                article.download()
                article_download_total = time.time() - article_download_start

                #get get urls from the article
                get_links_start = time.time()
                links = article.get_links()
                get_links_total = time.time() - get_links_start

                process_links_start = time.time()
                for link in links:
                    url = urljoin(current_url, link.href, False)
                    if self.url_in_filter(url, self.filters):
                        logging.info("skipping url \"{0}\" because it matches filter".format(url))
                        continue
                    try:
                        parsed_url = urlparse(url)
                        parsed_as_list = list(parsed_url)
                        if(parsed_url.scheme != u"http" and parsed_url.scheme != u"https"):
                            logging.info(u"skipping url with invalid scheme: {0}".format(url))
                            continue
                        parsed_as_list[5] = ''
                        url = urlunparse(urlnorm.norm_tuple(*parsed_as_list))
                    except Exception as e:
                        logging.info(u"skipping malformed url {0}. Error: {1}".format(url, str(e)))
                        continue
                    if(not parsed_url.netloc.endswith(self.domain)):
                        continue

                    #when executing an INSERT statement cursor.execute returns the number of rows updated. If the url
                    #exists in the visited table, then no rows will be updated. Thus if a row is updated, we know that
                    #it has not been visited and we should add it to the visit queue
                    self.cursor.execute(u"SELECT EXISTS(SELECT * FROM " + self.visited_table + " WHERE url=%s)",(url,))
                    self.transactions_file.write("2" + url+"\n")
                    if(self.cursor.fetchone()[0]):
                        continue

                    self.cursor.execute(u"INSERT INTO " + self.tovisit_table + u" VALUES (DEFAULT , %s)", (url,))
                    self.cursor.execute(u"INSERT INTO " + self.visited_table + u" VALUES (%s)", (url,))
                    self.transactions_file.write("3" + url+"\n")
                    logging.info(u"added {0} to the visit queue".format(url))
                self.db.commit()
                process_links_total = time.time() - process_links_start
                profile_data = [tovisit_pop_total, article_download_total, get_links_total, len(links), process_links_total]
                self.pages_visited += 1
                return (article, profile_data)
        except Exception as e:
            raise e
        finally:
            self.db.commit()
            self.transactions_file.flush()

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
        """
        Checks if any of the filters matches the url.
        Filters can be in regex search or normal string comparison.
        """
        for filt in filters:
            if ((filt.regex and re.search(filt.pattern, url, re.IGNORECASE)) or
                (not filt.regex and filt.pattern in url)):
                return True
        return False
