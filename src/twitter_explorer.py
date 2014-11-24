import datetime
import tweepy
import time
import re
import urllib2
from tld import get_tld
from tld.utils import update_tld_names
import timeit

import sys
import os
import django
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Frontend')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'

from tweets.models import*
from tweets.models import Keyword as T_keyword
from explorer.models import*
from explorer.models import Keyword as E_keyword


__author__ = "ACME: CSCC01F14 Team 4"
__authors__ = "Yuya Iwabuchi, Jai Sughand, Xiang Wang, Kyle Bridgemohansingh, Ryan Pan"

## FOLLOWING GLOBAL VARIABLES ARE NOW HANDLED BY config.yaml
##  and configuration()
# -----------------------------------------------------------------------
# Twitter Developer API
#CONSUMER_KEY = "UITySH5N4iGOE3l6C0YgmwHVd"
#CONSUMER_SECRET = "H7lXeLBDQv3o7i4wISGJtukdAqC6X9Vr4EXTdaIAVVrN56Lwbh"
#ACCESS_TOKEN = "2825329492-TKU4s0Mky7vazr60WKHQV7R6sJT2wYE4ysR3Gm3"
#ACCESS_TOKEN_SECRET = "I740fF6x6v0srzbY7LCAjNWXXOzZRMBFbkoiwZ5FgqC5s"

# Globals to be used for Database
#STORE_ALL_SOURCES = False
#DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


#INIT_TWEET_COUNT=1000
#ITER_TWEET_COUNT=100

#FROM_START = True
#MIN_ITERATION_TIME = 600

#Seconds to wait before retrying call
#WAIT_RATE = (60 * 1) + 0

# Used for commmunication stream
#COMM_FILE = '_comm.stream'
#RETRY_COUNT = 10
#RETRY_DELTA = 1
#SLEEP_TIME = 5

# -----------------------------------------------------------------------

def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open("../config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    #Config is returned as a dictionary, which you can navigate through later to get
    #a specific setting
    return config

def authorize():
    """ (None) -> tweepy.API
    Will use global keys to allow use of API
    """
    #Get's config settings for twitter
    config = configuration()['twitter']
    #Authorizing use with twitter development api
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    return tweepy.API(auth)

def wait_and_resume():
    """ (None) -> None
    Helper function to be called when a rate limit has been reached.
    """
    wait_rate = configuration()["twitter"]['wait_rate_seconds']
    print ('Twitter Rate Limit Reached, Attempting to Continue.')
    print ('Resuming in ' + str(int(wait_rate/60)) + ' minute(s) and '
                   + str(wait_rate % 60) + ' second(s).')
    time.sleep(wait_rate)

def get_tweets(screen_name, amount):
    """ (str, [int]) -> list of list
    Gets amount tweets from specified users
    Returns list in format [uni tweet, uni user, str time_tweeted]

    Keyword arguments:
    screen_name     -- string of twitter handle
    sites           -- List of string site urls to look for
    """

    tweet_holder=[]
    api = authorize()

    #Make sure 3190 is max tweets to get, while making sure
    #the amount of tweets to get is under the amount the user has.
    user = api.get_user(screen_name)
    if amount > 3190 or amount > user.statuses_count:
        amount = min(3190, user.statuses_count)

    #Basically acts as an iterator
    items = tweepy.Cursor(api.user_timeline,id= screen_name,
                          count = 200, include_rts=True).items()

    count = 0
    while count != amount:
        try:
            #Get's next tweet and appends to holder
            item = next(items)
            count += 1
            tweet_holder.append(item)
        except:
            #If error occurs (timeout)
            wait_and_resume()
            continue
    return tweet_holder

def get_follower_count(screen_name):
    """ (str) -> int
    Gets number of followers of screen_name's account

    Keyword arguments:
    screen_name     -- string of twitter handle
    """
    api = authorize()
    while True:
        try:
            user = api.get_user(screen_name)
            return user.followers_count
        except:
            wait_and_resume()

def get_keywords(tweet, keywords):
    """ (status, list of str) -> list of str
    Searches and returns keywords contained in the tweet
    Returns empty list otherwise.

    Keyword arguments:
    tweet           -- Status structure to be searched through
    sites           -- List of keywords to look for
    """
    matched_keywords = []

    #Searches if keyword is in tweet regardless of casing
    for key in keywords:
        if re.search(key, tweet.text.encode('utf8'), re.IGNORECASE):
            matched_keywords.append(key)


    matched_in_url = []
    expanded_urls = ''
    display_urls = ''
    for url in tweet.entities['urls']:
        try:
            # tries to get full url on shortened urls
            expanded_urls += urllib2.urlopen(url['expanded_url']).geturl() + ' '
            expanded_urls += urllib2.urlopen(url['display_url']).geturl() + ' '
        except:
            #if not just take normal url
            expanded_urls += url['expanded_url'] + ' '
            display_urls += url['display_url'] + ' '

    #substring, expanded includes scheme, display may not
    #uses two large url strings, rather than having n^2 complexity
    for keyword in keywords:
        if re.search(keyword, expanded_urls, re.IGNORECASE) or re.search(keyword, display_urls, re.IGNORECASE):
            matched_in_url.append(keyword)
    #Uses get_sources, but instead of searching tweets, searches
    #Adds both searches
    all_matches = matched_keywords + matched_in_url
    all_matches = set(all_matches)
    return list(all_matches)

def get_sources(tweet, sites):
    """ (status, list of str) -> list of str
    Searches and returns links redirected to sites within the urls
    of the tweet
    Returns empty list if none found

    Keyword arguments:
    tweet           -- Status structure to be searched through
    sites           -- List of site urls to look for
    """
    # store_all = configuration()['storage']['store_all_sources']

    matched_urls = []
    tweet_urls = []
    #if store_all == False:
    for url in tweet.entities['urls']:
        try:
            # tries to get full url on shortened urls
            tweet_urls.append(urllib2.urlopen(url['expanded_url']).geturl())
        except:
            #if not just take normal url
            tweet_urls.append(url['expanded_url'])

    #substring, expanded includes scheme, display may not
    for site in sites:
        for url in tweet_urls:
            if re.search(site, url, re.IGNORECASE) or re.search(site, url, re.IGNORECASE):
                matched_urls.append([url, site]) # should store [whole source, 'site' url]
    # elif store_all == True:
    #     for url in tweet.entities['urls']:
    #         try:
    #             # tries to get full url on shortened urls
    #             matched_urls.append([urllib2.urlopen(url['expanded_url']).geturl(),
    #                                 site]) # should store [whole source, 'site' url]
    #
    #         except:
    #             matched_urls.append([url['expanded_url'],
    #                                 site])  # should store [whole source, 'site' url]

    return matched_urls

def parse_tweets(twitter_users, keywords, foreign_sites, tweet_number):
    """ (list of str, list of str, list of str, str) -> none
    Parses through tweets of users, looking for keywords and foreign sites.
    Relevant tweets will be sent to a database.

    Keyword arguments:
    twitter_users   -- List of strings as twitter handles
    keywords        -- List of strings as keywords to search for
    foreign_sites   -- List of strings as sources to search for
    db_name         -- String of Database
    """
    config = configuration()['storage']
    django.setup()
    added, updated, no_match = 0, 0, 0
    start = time.time()

    for user in twitter_users:
        # Check for any new command on communication stream
        check_command()
        processed = 0
        # print "Parsing @" + user
        tweets = get_tweets(user, tweet_number)
        tweet_followers = get_follower_count(user)
        tweet_count = len(tweets)
        for tweet in tweets:
            # Check for any new command on communication stream
            check_command()

            # print '\tEvaluating ...\r'
            tweet_id = tweet.id
            tweet_date = tweet.created_at
            tweet_date
            tweet_user = tweet.user.screen_name
            tweet_store_date = datetime.datetime.now().strftime(config['date_format'][1:])
            tweet_keywords = get_keywords(tweet, keywords)
            tweet_sources = get_sources(tweet, foreign_sites)
            tweet_text = tweet.text

            # print "\tTweet:    ", tweet.text
            # print "\tAuthor:   ", tweet_user
            # print "\tDate:     ", tweet_date
            # print "\tKeywords: ", tweet_keywords
            # print "\tSources:  ", tweet_sources
            # print "\n"

            if not(tweet_keywords == [] and (tweet_sources ==[] or config['store_all_sources'])):

                tweet_list = Tweet.objects.filter(tweet_id = tweet_id)
                if (not tweet_list): 

                    tweet = Tweet(tweet_id = tweet_id, user=tweet_user, 
                                  date_added = tweet_store_date, 
                                  date_published = tweet_date, 
                                  followers = tweet_followers, text=tweet_text)
                    tweet.save()

                    tweet =  Tweet.objects.get(tweet_id=tweet_id)
                    
                    for key in tweet_keywords:
                        tweet.keyword_set.create(keyword = key)
       
                    for source in tweet_sources:
                        tweet.source_set.create(url = source[0], 
                                                url_origin=source[1])

                    added += 1
                    # print "\tResult:    Match detected! Added to the database."

                else:

                    tweet = tweet_list[0]
                    tweet.text = tweet_text
                    tweet.tweet_id = tweet_id
                    tweet.user = tweet_user 
                    # tweet.date_added = tweet_store_date
                    tweet.date_published = tweet_date
                    tweet.followers = tweet_followers
                    tweet.save()

                    for key in tweet_keywords:
                        if not T_keyword.objects.filter(keyword=key): 
                            tweet.keyword_set.create(keyword=key)

                    for source in tweet_sources:
                        if not Source.objects.filter(url=source[0]):
                            tweet.source_set.create(url=source[0], url_origin=source[1])
                    # print "\tResult:    Match detected! Tweet already in database. Updating."
                    updated += 1

            else:
                no_match += 1
            processed += 1
            sys.stdout.write("(Twitter|%s) %i/%i          \r" % (user, processed, tweet_count))
            sys.stdout.flush()
        print format("(Twitter|%s) %i/%i          " % (user, processed, tweet_count))
        #         print "\tResult:    No Match Detected."
        # print("\n\tStatistics\n\tAdded: %i | Updated: %i | No Match: %i | Time Elapsed: %is" %
          # (added, updated, no_match, time.time() - start))
    #     print "+--------------------------------------------------------------------+"

    # print("Finished parsing all users!")


def explore(accounts_db, keyword_db, site_db, tweet_number):
    """ (str, str, str, str) -> None
    Connects to accounts, keyword and site database, crawls within monitoring sites,
    then pushes articles which matches the keywords or foreign sites to the tweet database

    Keyword arguments:
    accounts_db         -- Twitter Accounts database name
    keyword_db          -- Keywords database name
    site_db             -- Sites database name
    tweet_db            -- Tweet database name
    """
    # print "+----------------------------------------------------------+"
    # print "| Retrieving data from Database ...                        |"
    # print "+----------------------------------------------------------+"

    # Connects to Site Database


    monitoring_sites = []
    msites = Msite.objects.all()
    # Retrieve, store, and print monitoring site information
    # print "\nMonitoring Sites\n\t%-25s%-40s" % ("Name", "URL")
    for site in msites:
        # monitoring_sites is now in form [['Name', 'URL'], ...]
        monitoring_sites.append([site.name, site.url])
        # print("\t%-25s%-40s" % (site.name, site.url))

    foreign_sites = []
    # Retrieve, store, and print foreign site information
    fsites = Fsite.objects.all()
    # print "\nForeign Sites\n\t%-25s%-40s" % ("Name", "URL")
    for site in fsites:
        # foreign_sites is now in form ['URL', ...]
        foreign_sites.append(site.url)
        # print("\t%-25s%-40s" % (site.name, site.url))


    # Retrieve all stored keywords
    keywords = E_keyword.objects.all()
    keyword_list = []

    # Print all the keywords
    # print "\nKeywords:"

    for key in keywords:
        keyword_list.append(str(key.keyword))
    #     print "\t%s" % key.keyword

    # print "\n"

    # print "+----------------------------------------------------------+"
    # print "| Populating Accounts ...                                  |"
    # print "+----------------------------------------------------------+"

    # Retrieve all stored Accounts
    accounts = Taccount.objects.all()
    accounts_list = []




    # Print all the Accounts
    # print "\nTwitter Accounts:"
    for account in accounts:
        accounts_list.append(str(account.account))
        # print "\t%s" % account.account


    # print "\n"

    # print "+----------------------------------------------------------+"
    # print "| Evaluating Tweets ...                                    |"
    # print "+----------------------------------------------------------+"
    # Parse the articles in all sites
    parse_tweets(accounts_list, keyword_list, foreign_sites, tweet_number)

def comm_write(text):
    config = configuration()['communication']
    for i in range(config['retry_count']):
        try:
            comm = open('twitter' + config['comm_file'], 'w')
            comm.write(text)
            comm.close()
            return None
        except:
            time.sleep(config['retry_delta'])

def comm_read():
    config = configuration()['communication']
    for i in range(config['retry_count']):
        try:
            comm = open('twitter' + config['comm_file'], 'r')
            msg = comm.read()
            comm.close()
            return msg
        except:
            time.sleep(config['retry_delta'])

def comm_init():
    comm_write('RR %s' % os.getpid())

def check_command():
    config = configuration()['communication']
    msg = comm_read()

    if msg[0] == 'W':
        command = msg[1]
        if command == 'S':
            print ('Stopping Explorer...')
            comm_write('SS %s' % os.getpid())
            sys.exit(0)
        elif command == 'P':
            print ('Pausing ...')
            comm_write('PP %s' % os.getpid())
            while comm_read()[1] == 'P':
                print ('Waiting %i seconds ...' % config['sleep_time'])
                time.sleep(config['sleep_time'])
            check_command()
        elif command == 'R':
            print ('Resuming ...')
            comm_write('RR %s' % os.getpid())

if __name__ == '__main__':
    # print configuration()
    # y = get_tweets('acmeteam4', 6000)
    x = get_tweets('kylebsingh',2)
    print get_keywords(x[0],['google.com', 'http://', 'goo'])

    # for g in x:
    #     print g.text

    # parse_tweets(['CNN', 'TIME'], ['obama','hollywood', 'not', 'fire', 'president', 'activities'], ['http://cnn.com/', 'http://ti.me'], 'tweets')
    
    #Initialize Communication Stream
    comm_init()
    config = configuration()['twitter']

    fs = config['from_start']

    while 1:
        # Check for any new command on communication stream
        check_command()

        start = timeit.default_timer()

        if (fs == True ):
            explore('taccounts', 'keywords', 'sites', config['initial_tweet_count'])
            fs = False
        else:
            explore('taccounts', 'keywords', 'sites', config['iteration_tweet_count'])

        end = timeit.default_timer()
        delta_time = end - start
        time.sleep(max(config['min_iteration_time']-delta_time, 0))
