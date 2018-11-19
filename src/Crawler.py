from urllib.parse import urlparse, urljoin, urlunparse
import random
import common
import re
import logging
from ExplorerArticle import ExplorerArticle
#import urlnorm
import urltools
import psycopg2
import os
import io
import sys
from pybloom_live import ScalableBloomFilter
from pqueue import Queue
from queue import Empty
from django.utils.text import slugify
import time

'''
An iterator class for iterating over articles in a given site
'''

class Crawler(object):
    def __init__(self, site):
        '''
        (Crawler, str) -> Crawler
        creates a Crawler with a given origin_url
        '''
        self.site = site
        self.filters = site.referringsitefilter_set.all()
        self.domain = urlparse(site.url).netloc
        # http://alexeyvishnevsky.com/2013/11/tips-on-optimizing-scrapy-for-a-high-performance/
        # fork of pybloom: https://github.com/joseph-fox/python-bloomfilter
        logging.info("c1")
        self.ignore_filter = ScalableBloomFilter(
                initial_capacity=10000000,
                error_rate=0.00001)
        ignore_filter_dir='../ignore_filter/'
        logging.info("c2")
        if not os.path.exists(ignore_filter_dir):
            os.makedirs(ignore_filter_dir)
            logging.info("c3")
            self.ignore_filter = ScalableBloomFilter(
                initial_capacity=10000000,
                error_rate=0.00001)
            logging.info("c4")
            try:
                logging.info("c5")

                f = open('../ignore_filter/' + self.site.name + '_ignore_file.txt', 'r+')
                f.write(self.ignore_filter)
            except IOError:
                logging.info("c6")
                f = open('../ignore_filter/' + self.site.name + '_ignore_file.txt', 'w+')
                logging.info("c7")
            f.close()
        else:
            logging.info("c8")
            if (not(os.path.exists('../ignore_filter/' + self.site.name + '_ignore_file.txt'))):
                f = open('../ignore_filter/' + self.site.name + '_ignore_file.txt', 'w+')
                f.close()
                logging.info("c9")

            logging.info("cWITH")
            time.sleep(2)
            with open('../ignore_filter/' + self.site.name + '_ignore_file.txt', 'r+', buffering=4096) as ignore_filter_file:
                logging.info("cWITH2")
                try:
                    logging.info("c10")
                    for line in ignore_filter_file:
                        self.ignore_filter.add(line.decode('utf8').rstrip())
                except Exception as e:
                    logging.info(str(e))
            ignore_filter_file.close()
        logging.info("c11")
        self.visited_count = 0

        tmpqueuetmp_dir='../tmpqueue/tmp/'
        if not os.path.exists(tmpqueuetmp_dir):
            os.makedirs(tmpqueuetmp_dir)
            logging.info("c12")
        slugified_name = slugify(str(site.name))
        tmpqueue_dir = '../tmpqueue/{}'.format(slugified_name)
        if not os.path.exists(tmpqueue_dir):
            os.makedirs(tmpqueue_dir)
        logging.info("c13")
        self.to_visit = Queue(tmpqueue_dir, tempdir=tmpqueuetmp_dir)

        # Initial url
        if (self.site.is_shallow == False):
            self.to_visit.put(site.url)
        else:
            self.to_visit.put((site.url, str(0)))
        logging.info("c14")
        # Limit
        self.limit = common.get_config()["crawler"]["limit"]
        # Specifies how deep the shallow crawler should go; "1" is the lowest option for this
        self.level = common.get_config()["crawler"]["level"]
        logging.info("c15")
        """
        self.probabilistic_n = common.get_config()["crawler"]["n"]
        self.probabilistic_k = common.get_config()["crawler"]["k"]

        self.db = psycopg2.connect(host='localhost',
                                   database=common.get_config()["crawler"]["postgresql"]["name"],
                                   user=common.get_config()["crawler"]["postgresql"]["user"],
                                   password=common.get_config()["crawler"]["postgresql"]["password"])

        self.cursor = self.db.cursor()
        self.already_added_urls = set()
        self.visited_table = "visited_" + str(site.id)
        self.tovisit_table = "tovisit_" + str(site.id)

        #self.cursor.execute("DROP TABLE IF EXISTS " + self.visited_table)
        #self.cursor.execute("CREATE TABLE " + self.visited_table + " (url VARCHAR(1024) PRIMARY KEY)")
        self.cursor.execute("DROP TABLE IF EXISTS " + self.tovisit_table)
        self.cursor.execute(u"CREATE TABLE " + self.tovisit_table + " (id SERIAL PRIMARY KEY, url VARCHAR(1024))")

        #self.cursor.execute(u"INSERT INTO " + self.visited_table + " VALUES (%s)", (site.url,))
        self.cursor.execute(u"INSERT INTO " + self.tovisit_table + " VALUES (DEFAULT, %s)", (site.url,))

        self.db.commit()
        """

    def __iter__(self):
        return self

    def __next__(self):
        '''
        (Crawler) -> newspaper.Article
        returns the next article in the sequence
        '''

        #standard non-recursive tree iteration
        with open('../ignore_filter/' + self.site.name + '_ignore_file.txt', 'a') as ignore_filter_file:
            try:
                current_level = 0
                while(True):
                    if (self.limit > 0 and self.visited_count > self.limit):
                        raise StopIteration('Limit reached: {:d}'.format(self.limit))
                    # if(self.pages_visited > self.probabilistic_n):
                    #     raise StopIteration
                    # self.cursor.execute("SELECT * FROM " + self.tovisit_table + " ORDER BY id LIMIT 1")
                    # row = self.cursor.fetchone()
                    # if(row):
                    #     row_id = row[0]
                    #     current_url = row[1]
                    #     self.cursor.execute("DELETE FROM " + self.tovisit_table + " WHERE id=%s", (row_id,))
                    # else:
                    #     raise StopIteration

                    # if(self._should_skip()):
                    #     logging.info(u"skipping {0} randomly".format(current_url))
                    #     continue
                    try:
                        if (self.site.is_shallow):
                            current = self.to_visit.get_nowait()
                            current_url = current[0]
                            current_level = current[1]
                            logging.info("Shallow on level {0} {1}".format(current_level, current_url))
                        else:
                            current_url = self.to_visit.get_nowait()
                    except Empty:
                        self.site.is_shallow = True # On line 26 the site gets set TO DELETE
                        self.to_visit.put((self.site.url, str(0)))
                        self.ignore_filter = ScalableBloomFilter(
                        initial_capacity=10000000,
                        error_rate=0.00001)
                        ignore_filter_file.close()
                        os.remove('../ignore_filter/' + self.site.name + '_ignore_file.txt')
                        logging.info("stopped iteration")
                        logging.info("{0}".format(self.site.url))
                        raise ZeroDivisionError


                    logging.info("visiting {0}".format(current_url))
                    self.visited_count += 1
                    #use newspaper to download and parse the article
                    article = ExplorerArticle(current_url)
                    article.download()
                    if (self.site.is_shallow):
                        if (int(current_level) > self.level):
                            continue
                    # get urls from the article
                    for link in article.get_links():
                        url = urljoin(current_url, link.href, False)
                        if self.url_in_filter(url, self.filters):
                            logging.info("skipping url \"{0}\" because it matches filter".format(url))
                            continue
                        try:
                            parsed_url = urlparse(url)
                            parsed_as_list = list(parsed_url)

                            if(parsed_url.scheme != "http" and parsed_url.scheme != "https"):
                                logging.info("skipping url with invalid scheme: {0}".format(url))
                                continue
                            parsed_as_list[5] = ''
                            url = urlunparse(urlnorm.norm_tuple(*parsed_as_list))
                        except Exception as e:
                            logging.info("skipping malformed url {0}. Error: {1}".format(url, str(e)))
                            continue
                        if(not parsed_url.netloc.endswith(self.domain)):
                            continue
                        # If the url have been added to ignore list, skip
                        if (url in self.ignore_filter):
                            continue
                        # Ignores the subscribe links for many domains
                        if ("subscribe" in url or "subscribe" in url and not("-subscribe" in url or "-subscribe" or "subscribe-" in url or "subscribe-")):
                        	continue

                        # Append the url to to_visit queue
                        if (self.site.is_shallow):
                            self.to_visit.put((url, str(int(current_level) + 1)))
                            logging.info("added {0} to the to_visit as well as the level {1}".format(url, str(int(current_level) + 1)))

                            # Append the url to visited to remove duplicates
                            self.ignore_filter.add(url)
                            ignore_filter_file.write(url.encode('utf8') + "\n")
                        else:
                            self.to_visit.put(url)
                            logging.info("added {0} to the to_visit".format(url))

                            # Append the url to visited to remove duplicates
                            self.ignore_filter.add(url)
                            ignore_filter_file.write(url.encode('utf8') + "\n")

                    # Update the Queue
                    self.to_visit.task_done()


                    return article


            except StopIteration as e:
                raise e
            except ValueError as e:
                raise ValueError
            except Exception as e:
                raise e

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

    # def __del__(self):
    #     self.cleanup()

    # def cleanup(self):
    #     if(self.db):
    #         self.db.close()
    #         self.db = None
    #     if(self.cursor):
    #         self.cursor.close()
    #         self.cursor = None

