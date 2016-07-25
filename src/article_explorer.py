"""
This script retrieves monitoring site, foreign sites,
and keywords from Django database and looks into the monitoring
sites to find matching foreign sites or keywords.
newspaper package is the core to extract and retrieve relevant data.
If any keyword (of text) or foreign sites (of links) matched,
the Article will be stored at Django database as articles.models.Article.
Django's native api is used to easily access and modify the entries.
"""

__author__ = "ACME: CSCC01F14 Team 4"
__authors__ = \
    "Yuya Iwabuchi, Jai Sughand, Xiang Wang, Kyle Bridgemohansingh, Ryan Pan"

import sys
import os

# Add Django directories in the Python paths for django shell to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
# newspaper, for populating articles of each site
# and parsing most of the data.
import newspaper
# Used for newspaper's keep_article_html as it was causing error without it
import lxml.html.clean
# Regex, for parsing keywords and sources
import re
# Mainly used to make the explorer sleep
import time
# For getting today's date with respect to the TZ specified in Django Settings
# For extracting 'pub_date's string into Datetime object
import dateutil
# To connect and use the Django Database

# To load configurations
import common
import Crawler
# To get domain from url
import tld

import logging
import glob
import datetime
# Custom ExlporerArticle object based on newspaper's Article
from ExplorerArticle import ExplorerArticle
# For multiprocessing

class FakeSite:
    def __init__(self):
        self.url = "http://theguardian.com/"
        self.id = 3

def parse_articles_per_site():
    processed = 0

    article_iterator = Crawler.Crawler(FakeSite()).__iter__()
    profile_log = open("profile.csv", "w")
    profile_log.write("total,crawler_total,preliminary_parse_total,explorer_article_total,get_keywords_total,get_sources_sites_total,get_sources_twitter_total,tovisit_pop_total,article_download_total,get_links_total,len(links),process_links_total\n")
    while True:
        total_start = time.time()
        crawler_total = -1
        preliminary_parse_total = -1
        explorer_article_total = -1
        get_keywords_total = -1
        get_sources_sites_total = -1
        get_sources_twitter_total = -1

        try:
            try:
                crawler_start = time.time()
                (article, crawler_profile_data) = article_iterator.next()
                crawler_total = time.time() - crawler_start
            except StopIteration:
                break
            #have to put all the iteration stuff at the top because I used continue extensively in this loop
            processed += 1
            print(processed)

            logging.info("Processing %s"%article.url)

            url = article.url
            if 'http://www.' in url:
                url = url[:7] + url[11:]
            elif 'https://www.' in url:
                url = url[:8] + url[12:]

            explorer_article_start = time.time()
            article = ExplorerArticle(article.url)
            explorer_article_total = time.time() - explorer_article_start
            logging.debug("ExplorerArticle Created")
            # Try to download and extract the useful data
            if(not article.is_downloaded):
                if(not article.download()):
                    logging.warning("article skipped because download failed")
                    continue
            url = article.canonical_url.strip()

            if (not article.is_parsed):
                preliminary_parse_start = time.time()
                result = article.preliminary_parse()
                preliminary_parse_total = time.time() - preliminary_parse_start
                if (not result):
                    logging.warning("article skipped because parse failed")
                    continue

            logging.debug("Article Parsed")
            
            logging.debug(u"Title: {0}".format(repr(article.title)))
            if not article.title:
                logging.info("article missing title, skipping")
                continue

            if not article.text:
                logging.info("article missing text, skipping")
                continue

            # Regex the keyword from the article's text
            get_keywords_start = time.time()
            keywords = get_keywords(article, ["paris", "middle east", "test", "israel", "gaza"])
            get_keywords_total = time.time() - get_keywords_start
            logging.debug(u"matched keywords: {0}".format(repr(keywords)))
            # Regex the links within article's html
            get_sources_sites_start = time.time()
            sources = get_sources_sites(article, [])
            get_sources_sites_total = time.time() - get_sources_sites_start
            logging.debug(u"matched sources: {0}".format(repr(sources)))
            get_sources_twitter_start = time.time()
            twitter_accounts = get_sources_twitter(article, [])
            get_sources_twitter_total = time.time() - get_sources_twitter_start
            logging.debug(u"matched twitter_accounts: {0}".format(repr(twitter_accounts[0])))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logging.exception("Unhandled exception while crawling: " + str(e))
        total = time.time() - total_start

        all_data = [total, crawler_total, preliminary_parse_total, explorer_article_total, get_keywords_total, get_sources_sites_total, get_sources_twitter_total] + crawler_profile_data
        all_data_str = [str(x) for x in all_data]
        profile_log.write(",".join(all_data_str) + "\n")
        profile_log.flush()



def url_in_filter(url, filters):
    """
    Checks if any of the filters matches the url.
    Filters can be in regex search or normal string comparison.    
    """
    for filt in filters:
        if ((filt.regex and re.search(filt.pattern, url, re.IGNORECASE)) or
            (not filt.regex and filt.pattern in url)):
            return True
    return False


def get_sources_sites(article, sites):
    """ (str, list of str) -> list of [str, str]
    Searches and returns links redirected to sites within the html
    links will be storing the whole url and the domain name used for searching.
    Returns empty list if none found

    Keyword arguments:
    html                -- string of html
    sites               -- list of site urls to look for
    """
    result_urls_matched = []
    result_urls_unmatched = []
    # Format the site to assure only the domain name for searching
    formatted_sites = set()

    for site in sites:
        formatted_sites.add(tld.get_tld(site))

    for url in article.get_links(article_text_links_only=True):
        try:
            domain = tld.get_tld(url.href)
        #apparently they don't inherit a common class so I have to hard code it
        except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound, tld.exceptions.TldIOError):
            continue
        if domain in formatted_sites:
            # If it matches even once, append the site to the list
            result_urls_matched.append([url.href, domain, url.text])
        else:
            result_urls_unmatched.append([url.href, domain, url.text])

    # Return the list
    return [result_urls_matched,result_urls_unmatched]


def get_sources_twitter(article, source_twitter):
    matched = []
    unmatched = []
    # Twitter handle name specifications
    accounts = re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', article.text)

    for account in set(accounts):
        if account in source_twitter:
            matched.append(account)
        else:
            unmatched.append(account)
    return [matched,unmatched]




def get_pub_date(article):
    """ (newspaper.article.Article) -> str
    Searches and returns date of which the article was published
    Returns None otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    """
    return article.newspaper_article.publish_date


def get_keywords(article, keywords):
    """ (newspaper.article.Article, list of str) -> list of str
    Searches and returns keywords which the article's title or text contains
    Returns empty list otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    keywords        -- List of keywords
    """
    matched_keywords = []

    # For each keyword, check if article's text contains it
    for key in keywords:
        regex = re.compile('[^a-z]' + key + '[^a-z]', re.IGNORECASE)
        if regex.search(article.title) or regex.search(article.get_text(strip_html=True)):
            # If the article's text contains the key, append it to the list
            matched_keywords.append(key)
    # Return the list
    return matched_keywords


def comm_write(text):
    """ (Str) -> None
    Writes a command to the comm_file of article.
    The file is used to communicate with the running explorer process,
    to change the status safely.

    Keyword arguments:
    text         -- String of command
    """
    # Load the relevant configs
    conf = common.get_config()['communication']

    # Wait for retry_count * retry_delta seconds
    for k in range(conf['retry_count']):
        try:
            comm = open('article' + conf['comm_file'], 'w')
            comm.write(text)
            comm.close()
            return None
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            time.sleep(conf['retry_delta'])


def comm_read():
    """ (None) -> Str
    Reads the current status or command listed on the comm_file with the
    article, then returns the output.
    """
    # Load the relevant configs
    conf = common.get_config()['communication']

    # Wait for retry_count * retry_delta seconds
    for k in range(conf['retry_count']):
        try:
            comm = open('article' + conf['comm_file'], 'r')
            msg = comm.read()
            comm.close()
            return msg
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            time.sleep(conf['retry_delta'])


def comm_init():
    """ (None) -> None
    Initialize The communication file
    """
    logging.debug("Initializing Communication Stream")
    pid = os.getpid()
    # Set the current status as Running
    logging.debug("Comm Status: RR %s" % pid)
    comm_write('RR %s' % pid)


def check_command():
    """ (None) -> None
    Check the communication file for any commands given.
    Execute according to the commands.
    """
    # Load the relevant configs
    logging.debug("Checking for any new command on communication stream")
    conf = common.get_config()['communication']
    msg = comm_read()

    # Let the output print back to normal for printing status
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    if msg[0] == 'W':
        command = msg[1]
        if command == 'S':
            print('Stopping Explorer...')
            logging.info("Stop command detected, Stopping.")
            comm_write('SS %s' % os.getpid())
            sys.exit(0)
        elif command == 'P':
            print('Pausing ...')
            logging.info("Pause command detected, Pausing.")
            comm_write('PP %s' % os.getpid())
            while comm_read()[1] == 'P':
                logging.info('Waiting %i seconds ...' % conf['sleep_time'])
                print('Waiting %i seconds ...' % conf['sleep_time'])
                time.sleep(conf['sleep_time'])
                check_command()
        elif command == 'R':
            print('Resuming ...')
            logging.info('Resuming.')
            comm_write('RR %s' % os.getpid())


def setup_logging(site_name="", increment=True):
    # Load the relevant configs
    config = common.get_config()

    # Logging config
    current_time = datetime.datetime.now().strftime('%Y%m%d')
    log_dir = config['projectdir']+"/log"
    prefix = log_dir + "/" + site_name + "article_explorer-"
    
    try:
        cycle_number = sorted(glob.glob(prefix + current_time + "*.log"))[-1][-7:-4]
        if increment:
            cycle_number = str(int(cycle_number) + 1)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        cycle_number = "0"

    # Remove all handlers associated with the root logger object.
    # This will allow logging per site
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=current_time + "-" + cycle_number.zfill(3) + ".log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    default_logger = logging.getLogger('')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(default_logger.handlers[0].formatter)
    default_logger.addHandler(console_handler)
    # Finish logging config


if __name__ == '__main__':
    parse_articles_per_site()
