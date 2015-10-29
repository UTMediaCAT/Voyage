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
# Append local python lib to the front to assure
# local library(mainly Django 1.7.1) to be used
sys.path.insert(0, os.path.join(os.environ['HOME'],
                                '.local/lib/python2.7/site-packages'))
# newspaper, for populating articles of each site
# and parsing most of the data.
import newspaper
# Used for newspaper's keep_article_html as it was causing error without it
import lxml.html.clean
# Regex, for parsing keywords and sources
import re
# Mainly used to make the explorer sleep
import time
import timeit
# For getting today's date with respect to the TZ specified in Django Settings
from django.utils import timezone
# For extracting 'pub_date's string into Datetime object
from dateutil import parser
# To connect and use the Django Database
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
# For Models connecting with the Django Database
from articles.models import*
from articles.models import Keyword as ArticleKeyword
from articles.models import SourceSite as ArticleSourceSite
from articles.models import SourceTwitter as ArticleSourceTwitter
from explorer.models import*
from explorer.models import SourceTwitter as ExplorerSourceTwitter
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceSite as ExplorerSourceSite
# To load configurations
import common
# To store the article as warc files
import warc_creator
import Crawler
# To get domain from url
import tld
# To concatenate newspaper's articles and Crawler's articles
import itertools
import requests
# For Logging
import logging
import glob
import datetime
# Custom ExlporerArticle object based on newspaper's Article
from ExplorerArticle import ExplorerArticle
# For multiprocessing
from multiprocessing import Pool, cpu_count
from functools import partial
import signal

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def parse_articles(referring_sites, db_keywords, source_sites, twitter_accounts_explorer):
    """ (list of [str, newspaper.source.Source, str],
         list of str, list of str, str) -> None
    Downloads each db_article in the site, extracts, compares
    with Foreign Sites and Keywords provided.
    Then the db_article which had a match will be stored into the Django database

    Keyword arguments:
    referring_sites     -- List of [name, 'built_article'] of each site
    db_keywords         -- List of keywords
    source_sites       -- List of foreign sites
    """
    added, updated, failed, no_match = 0, 0, 0, 0

    # Initialize multiprocessing by having cpu*4 workers
    pool = Pool(processes=cpu_count()*4, maxtasksperchild=1, initializer=init_worker)

    # pass database informations using partial
    pass_database = partial(parse_articles_per_site, db_keywords, source_sites, twitter_accounts_explorer)

    # Start the multiprocessing
    result = pool.map_async(pass_database, referring_sites)

    # Continue until all sites are done crawling
    while (not result.ready()):
        try:
            # Check for any new command on communication stream
            check_command()
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit) as e:
            logging.warning("%s detected, exiting"%str(e))
            sys.exit(0)
    
    # Fail-safe to ensure the processes are done
    pool.close()
    pool.join()



def parse_articles_per_site(db_keywords, source_sites, twitter_accounts_explorer, site):

    logging.info("Started multiprocessing of Site: %s", site['name'])
    #Setup logging for this site
    setup_logging(site['name'])

    article_count = 0
    newspaper_articles = []
    crawlersource_articles = []
    logging.info("Site: %s Type:%i"%(site['name'], site['type']))
    #0 = newspaper, 1 = crawler, 2 = both

    if(site["type"] == 0 or site["type"] == 2):
        logging.disable(logging.ERROR)
        newspaper_source = newspaper.build(site["url"],
                                         memoize_articles=False,
                                         keep_article_html=True,
                                         fetch_images=False,
                                         language='en',
                                         number_threads=1)
        logging.disable(logging.NOTSET)
        newspaper_articles = newspaper_source.articles
        article_count += newspaper_source.size()
        logging.info("populated {0} articles using newspaper".format(article_count))
    if(site["type"] == 1 or site["type"] == 2):
        crawlersource_articles = Crawler.Crawler(site["url"], site["filter"])
        article_count += crawlersource_articles.probabilistic_n
        logging.debug("expecting {0} from plan b crawler".format(crawlersource_articles.probabilistic_n))
    article_iterator = itertools.chain(iter(newspaper_articles), crawlersource_articles).__iter__()
    processed = 0
    while True:
        try:
            try:
                article = article_iterator.next()
            except StopIteration:
                break
            #have to put all the iteration stuff at the top because I used continue extensively in this loop
            processed += 1

            if url_in_filter(article.url, site["filter"]):
                logging.info("Matches with filter, skipping the {0}".format(article.url))
                continue

            print(
                "%s (Article|%s) %i/%i          \r" %
                (str(timezone.localtime(timezone.now()))[:-13],
                 site["name"], processed, article_count))
            logging.info("Processing %s"%article.url)

            url = article.url
            if 'http://www.' in url:
                url = url[:7] + url[11:]
            elif 'https://www.' in url:
                url = url[:8] + url[12:]
            article = ExplorerArticle(article.url)
            logging.debug("ExplorerArticle Created")
            # Try to download and extract the useful data
            if(not article.is_downloaded):
                if(not article.download()):
                    logging.warning("article skipped because download failed")
                    continue

            if (not article.is_parsed):
                if (not article.preliminary_parse()):
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
            keywords = get_keywords(article, db_keywords)
            logging.debug(u"matched keywords: {0}".format(repr(keywords)))
            # Regex the links within article's html
            sources = get_sources_sites(article, source_sites)
            logging.debug(u"matched sources: {0}".format(repr(sources)))
            twitter_accounts = get_sources_twitter(article, twitter_accounts_explorer)
            logging.debug(u"matched twitter_accounts: {0}".format(repr(twitter_accounts[0])))

            if((not keywords) and (not sources[0]) and (not twitter_accounts[0])):#[] gets coverted to false
                logging.debug("skipping article because it's not a match")
                continue
            logging.info("match found")

            article.newspaper_parse()

            authors = article.authors
            pub_date = get_pub_date(article)
            # Check if the entry already exists
            db_article_list = Article.objects.filter(url=url)
            if not db_article_list:
                logging.info("Adding new Article to the DB")
                # If the db_article is new to the database,
                # add it to the database
                db_article = Article(title=article.title, url=url,
                                  domain=site["url"],
                                  date_added=timezone.localtime(
                                      timezone.now()),
                                  date_published=pub_date)
                db_article.save()

                db_article = Article.objects.get(url=url)

                for key in keywords:
                    db_article.keyword_set.create(name=key)

                for author in authors:
                    db_article.author_set.create(name=author)
                for account in twitter_accounts[0]:

                    db_article.sourcetwitter_set.create(name = account, matched = True)

                for account in twitter_accounts[1]:
                    db_article.sourcetwitter_set.create(name = account, matched = False)

                for source in sources[0]:
                    db_article.sourcesite_set.create(url=source[0],
                                              domain=source[1], matched=True, local=(source[1] in site["url"]))

                for source in sources[1]:
                    db_article.sourcesite_set.create(url=source[0],
                                              domain=source[1], matched=False, local=(source[1] in site["url"]))

            else:
                logging.info("Modifying existing Article in the DB")
                # If the db_article already exists,
                # update all fields except date_added
                db_article = db_article_list[0]
                db_article.title = article.title
                db_article.url = url
                db_article.domain = site["url"]
                # Do not update the added date
                # db_article.date_added = today
                db_article.date_published = pub_date
                db_article.save()

                for key in keywords:
                    if not db_article.keyword_set.filter(name=key):
                        db_article.keyword_set.create(name=key)

                for author in authors:
                    if not db_article.author_set.filter(name=author):
                        db_article.author_set.create(name=author)

                for account in twitter_accounts[0]:
                    if not db_article.sourcetwitter_set.filter(name=account):
                        db_article.sourcetwitter_set.create(name = account, matched = True)

                for account in twitter_accounts[1]:
                    if not db_article.sourcetwitter_set.filter(name=account):
                        db_article.sourcetwitter_set.create(name = account, matched = False)

                for source in sources[0]:
                    if not db_article.sourcesite_set.filter(url=source[0]):
                        db_article.sourcesite_set.create(url=source[0],
                                              domain=source[1], matched=True, local=(source[1] in site["url"]))

                for source in sources[1]:
                    if not db_article.sourcesite_set.filter(url=source[0]):
                        db_article.sourcesite_set.create(url=source[0],
                                              domain=source[1], matched=False, local=(source[1] in site["url"]))

            warc_creator.create_article_warc(url)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logging.exception("Unhandled exception while crawling: " + str(e))

    logging.info("Finished Site: %s"%site['name'])
    setup_logging(increment=False)
    logging.info("Finished Site: %s"%site['name'])

def url_in_filter(url, filters):
    """
    Checks if any of the filters matches the url.
    Filters can be in regex search or normal string comparison.    
    """
    for filt in filters:
        if ((filt[1] and re.search(filt[0], url, re.IGNORECASE)) or
            (not filt[1] and filt[0] in url)):
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

    for url in article.get_urls(article_text_links_only=True):
        try:
            domain = tld.get_tld(url)
        #apparently they don't inherit a common class so I have to hard code it
        except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound, tld.exceptions.TldIOError):
            continue
        if domain in formatted_sites:
            # If it matches even once, append the site to the list
            result_urls_matched.append([url, domain])
        else:
            result_urls_unmatched.append([url, domain])

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
    dates = []

    # For each metadata stored by newspaper's parsing ability,
    # check if any of the key contains 'date'
    for key, value in article.newspaper_article.meta_data.iteritems():
        if re.search("date", key, re.IGNORECASE):
            # If the key contains 'date', try to parse the value as date
            try:
                dt = parser.parse(str(value))
                # If parsing succeeded, then append it to the list
                dates.append(dt)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pass
    # If one of more dates were found,
    # return the oldest date as new ones can be updated dates
    # instead of published date
    if dates:
        date = sorted(dates, key=lambda x: str(x)[0])[0]
        if timezone.is_naive(date):
            return \
                timezone.make_aware(date,
                                    timezone=timezone.get_default_timezone())
        else:
            return timezone.localtime(date)
    return None


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
        if regex.search(article.title) or regex.search(article.text):
            # If the article's text contains the key, append it to the list
            matched_keywords.append(key)
    # Return the list
    return matched_keywords


def explore():
    """ () -> None
    Connects to keyword and site tables in database,
    crawls within monitoring sites, then pushes articles which matches the
    keywords or foreign sites to the article database
    """

    # Retrieve and store monitoring site information
    referring_sites = []
    index = 0
    for site in ReferringSite.objects.all():
        referring_sites.append({"name":site.name, "url":site.url, "type":site.mode, "filter":[]})
        for filt in site.referringsitefilter_set.all():
            referring_sites[index]["filter"].append([filt.pattern, filt.regex])
        index += 1
    logging.info("Collected {0} Referring Sites from Database".format(len(referring_sites)))

    # Retrieve and store foreign site information
    source_sites = []
    for site in ExplorerSourceSite.objects.all():
        # source_sites is now in form ['URL', ...]
        source_sites.append(site.url)
    logging.info("Collected {0} Source Sites from Database".format(len(source_sites)))

    # Retrieve all stored keywords
    keyword_list = []
    for key in ExplorerKeyword.objects.all():
        keyword_list.append(str(key.name))
    logging.info("Collected {0} Keywords from Database".format(len(keyword_list)))

    # Retrieve all stored twitter_accounts
    source_twitter_list = []
    twitter_accounts = ExplorerSourceTwitter.objects.all()
    for key in twitter_accounts:
        source_twitter_list.append(str(key.name))
    logging.info("Collected {0} Source Twitter Accounts from Database".format(len(source_twitter_list)))

    # Parse the articles in all sites
    parse_articles(referring_sites, keyword_list, source_sites, source_twitter_list)

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

    logging.basicConfig(filename=prefix + current_time + "-" + cycle_number.zfill(3) + ".log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    default_logger = logging.getLogger('')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(default_logger.handlers[0].formatter)
    default_logger.addHandler(console_handler)
    # Finish logging config


if __name__ == '__main__':
    # Load the relevant configs
    config = common.get_config()['article']

    # Main logging
    setup_logging()

    # Connects to Site Database
    logging.debug("Connecting to django/database")
    django.setup()
    logging.debug("Connected to django/database")

    # Initialize Communication Stream

    comm_init()

    # Check for any new command on communication stream
    check_command()

    start = timeit.default_timer()

    # The main function, to explore the articles
    explore()
    delta_time = timeit.default_timer() - start
    logging.info("Exploring Ended. Took %is"%delta_time)

    sleep_time = max(config['min_iteration_time']-delta_time, 0)
    logging.warning("Sleeping for %is"%sleep_time)
    for i in range(int(sleep_time//5)):
        time.sleep(5)
        check_command()
    check_command()

    # Re run the program to avoid thread to increase
    logging.info("Starting new cycle")
    os.chmod('article_explorer_run.sh', 0700)
    os.execl('article_explorer_run.sh', '')
