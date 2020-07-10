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
import dateutil
# To connect and use the Django Database
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
# For Models connecting with the Django Database
from articles.models import*
from articles.models import Keyword as ArticleKeyword
from articles.models import SourceSite as ArticleSourceSite
from articles.models import SourceTwitter as ArticleSourceTwitter
from articles.models import Version as ArticleVersion

from articles.models import Url as ArticleUrl
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
from ExplorerArticleJsonIssue import ExplorerArticleJsonIssue
# For multiprocessing
from multiprocessing import Pool, cpu_count, Process, Lock
from functools import partial
import signal
from django.db import connection
# For hashing the text
import hashlib

import time
from threading import Event, Thread

lock = Lock()
queue = []

import json
import collections
import time
import subprocess as sp
Link = collections.namedtuple("Link", ["href", "text"])

# For handling keyboard inturrupt
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def quick_get_links():

    # article_url = "https://www.jpost.com/Business-and-Innovation/Health-and-Science/Israeli-founded-start-up-raises-15m-to-help-fight-heart-failure-506353" 
    # json problem
    # article_url = 'https://www.theguardian.com/education/2020/jun/01/schools-expect-half-of-pupils-will-stay-home-as-year-groups-return'


    article_url = "https://tech.newstatesman.com/news/university-computer-science-admissions-rising-gender-gap"
    print("starting this")
    article = ExplorerArticle(article_url)
    # article = ExplorerArticleJsonIssue(article_url)
    print("finished explorer article")
    print("start get_links_crawl")
    links = article.get_links_crawl(article_text_links_only=True)
    print("end get_links_crawl")

    for url in links:
        print(url)

if __name__ == '__main__':
    quick_get_links()