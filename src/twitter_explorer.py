
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


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'


# For getting today's date
from django.utils import timezone

from tweets.models import*
from tweets.models import Keyword as TwitterKeyword
from tweets.models import SourceSite as TwitterSourceSite
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceTwitter as ExplorerSourceTwitter
from explorer.models import Keyword as ExplorerKeyword
import tld
# To store the article as warc files
import warc_creator

__author__ = "ACME: CSCC01F14 Team 4"
__authors__ = "Yuya Iwabuchi, Jai Sughand, Xiang Wang," \
              " Kyle Bridgemohansingh, Ryan Pan"


def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the parent directory from this file
    """
    # unit tests clause
    if "unit_tests" == os.getcwd().split("/")[-1]:
        config_yaml = open("../../config.yaml", 'r')
    else:
        config_yaml = open("../config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    # Config is returned as a dictionary, which you can navigate through
    # later to get a specific setting
    return config


def authorize():
    """ (None) -> tweepy.API
    Will use global keys to allow use of API
    """
    # Get's config settings for twitter
    config = configuration()['twitter']
    # Authorizing use with twitter development api
    auth = tweepy.OAuthHandler(
        config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(
        config['access_token'], config['access_token_secret'])
    return tweepy.API(auth)


def wait_and_resume():
    """ (None) -> None
    Helper function to be called when a rate limit has been reached.
    """
    wait_rate = configuration()["twitter"]['wait_rate_seconds']
    print('Twitter Rate Limit Reached, Attempting to Continue.')
    print('Resuming in ' + str(int(wait_rate / 60)) + ' minute(s) and '
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

    tweet_holder = []
    api = authorize()

    # Make sure 3190 is max tweets to get, while making sure
    # the amount of tweets to get is under the amount the user has.
    try:
        user = api.get_user(screen_name)
    except:
        wait_and_resume()
    if amount > 3190 or amount > user.statuses_count:
        amount = min(3190, user.statuses_count)

    # Basically acts as an iterator
    items = tweepy.Cursor(api.user_timeline, id=screen_name,
                          count=200, include_rts=True).items()

    count = 0
    while count != amount:
        try:
            # Get's next tweet and appends to holder
            item = next(items)
            count += 1
            tweet_holder.append(item)
        except:
            # If error occurs (timeout)
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


def geTwitterKeywords(tweet, keywords):
    """ (status, list of str) -> list of str
    Searches and returns keywords contained in the tweet
    Returns empty list otherwise.

    Keyword arguments:
    tweet           -- Status structure to be searched through
    keywords        -- List of keywords to look for
    """
    matched_keywords = []

    # Searches if keyword is in tweet regardless of casing
    for key in keywords:
        if re.search(key, tweet.text.encode('utf8'), re.IGNORECASE):
            matched_keywords.append(key)

    matched_in_url = []
    expanded_urls = ''
    display_urls = ''
    for url in tweet.entities['urls']:
        try:
            # tries to get full url on shortened urls
            expanded_urls += urllib2.urlopen(
                url['expanded_url']).geturl() + ' '
            expanded_urls += urllib2.urlopen(url['display_url']).geturl() + ' '
        except:
            # if not just take normal url
            expanded_urls += url['expanded_url'] + ' '
            display_urls += url['display_url'] + ' '

    # substring, expanded includes scheme, display may not
    # uses two large url strings, rather than having n^2 complexity
    for keyword in keywords:
        if re.search(keyword, expanded_urls, re.IGNORECASE) or \
                re.search(keyword, display_urls, re.IGNORECASE):
            matched_in_url.append(keyword)
    # Uses get_sources, but instead of searching tweets, searches
    # Adds both searches
    all_matches = matched_keywords + matched_in_url
    all_matches = set(all_matches)
    return list(all_matches)


def get_source_sites(tweet, sites):
    """ (status, list of str) -> list of str
    Searches and returns links redirected to sites within the urls
    of the tweet
    Returns empty list if none found

    Keyword arguments:
    tweet           -- Status structure to be searched through
    sites           -- List of site urls to look for
    """
    # store_all = configuration()['storage']['store_all_sources']

    hdr = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11' +
        ' (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    result_urls_matched = []
    result_urls_unmatched = []
    tweet_urls = []

    formatted_sites = []

    for site in sites:
        formatted_sites.append(tld.get_tld(site))

    # if store_all == False:
    for url in tweet.entities['urls']:
        try:
            # tries to get full url on shortened urls
            req = urllib2.Request(url['expanded_url'], headers=hdr)
            tweet_urls.append(str(urllib2.urlopen(req).url))

        except:
            # if not just take normal url
            tweet_urls.append(str(url['expanded_url']))

    # substring, expanded includes scheme, display may not
    for url in tweet_urls:
            try:
                domain = tld.get_tld(url[6:-1])
            except:
                continue
            if domain in formatted_sites:
                # If it matches even once, append the site to the list
                result_urls_matched.append([url[6:-1], domain])
            else:
                result_urls_unmatched.append([url[6:-1], domain])




    return [result_urls_matched,result_urls_unmatched]


def get_sources_twitter(tweet_text, source_twitter):
    matched = []
    unmatched = []
    # Twitter handle name specifications
    accounts = re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', tweet_text)

    for account in set(accounts):
        if account[1:] in source_twitter:
            matched.append(account)
        else:
            unmatched.append(account)
    return [matched,unmatched]


def parse_tweets(twitter_users, keywords, source_sites, tweet_number, source_twitter_list):
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
        tweets = get_tweets(user, tweet_number)
        tweet_followers = get_follower_count(user)
        tweet_count = len(tweets)

        for tweet in tweets:
            # Check for any new command on communication stream
            check_command()


            #setting correct data for each field
            tweet_id = tweet.id
            tweet_date = timezone.localtime(
                timezone.make_aware(tweet.created_at,
                                    timezone=timezone.get_fixed_timezone(180)))
            tweet_user = tweet.user.screen_name
            tweet_store_date = timezone.localtime(timezone.now())
            tweet_keywords = geTwitterKeywords(tweet, keywords)
            tweet_sources = get_source_sites(tweet, source_sites)
            twitter_accounts= get_sources_twitter(tweet.text, source_twitter_list)
            tweet_text = tweet.text

            if not(tweet_keywords == [] and tweet_sources[0] == [] and twitter_accounts[0] ==[]):

                tweet_list = Tweet.objects.filter(tweet_id=tweet_id)
                if (not tweet_list):
                    #creating new intry in collection
                    tweet = Tweet(tweet_id=tweet_id, name=tweet_user,
                                  date_added=tweet_store_date,
                                  date_published=tweet_date,
                                  text=tweet_text)
                    tweet.save()

                    tweet = Tweet.objects.get(tweet_id=tweet_id)

                    for account in twitter_accounts[0]:
                        tweet.sourcetwitter_set.create(name = account, matched = True)

                    for account in twitter_accounts[1]:
                        tweet.sourcetwitter_set.create(name = account, matched = False)

                    for key in tweet_keywords:
                        tweet.keyword_set.create(name=key)

                    for source in tweet_sources[0]:
                        tweet.sourcesite_set.create(url=source[0],
                                                domain=source[1], matched = True)
                    for source in tweet_sources[1]:
                        tweet.sourcesite_set.create(url=source[0],
                                                domain=source[1], matched = False)

                    added += 1

                else:

                    tweet = tweet_list[0]
                    tweet.text = tweet_text
                    tweet.tweet_id = tweet_id
                    tweet.name = tweet_user
                    # tweet.date_added = tweet_store_date
                    tweet.date_published = tweet_date
                    tweet.save()

                    for key in tweet_keywords:
                        if not TwitterKeyword.objects.filter(name=key):
                            tweet.keyword_set.create(name=key)

                    for source in tweet_sources[0]:
                        if not TwitterSourceSite.objects.filter(url=source[0]):
                            tweet.sourcesite_set.create(
                                url=source[0], domain=source[1],matched = True)

                    for source in tweet_sources[1]:
                        if not TwitterSourceSite.objects.filter(url=source[0]):
                            tweet.sourcesite_set.create(
                                url=source[0], domain=source[1],matched = False)

                    for account in twitter_accounts[0]:
                        tweet.sourcetwitter_set.create(name = account, matched = True)

                    for account in twitter_accounts[1]:
                        tweet.sourcetwitter_set.create(name = account, matched = False)

                    updated += 1

                warc_creator.create_twitter_warc(
                    'https://twitter.com/' + tweet.name + '/status/' +
                    str(tweet_id))
            else:
                no_match += 1
            processed += 1
            sys.stdout.write("%s (Twitter|%s) %i/%i          \r" %
                             (str(timezone.localtime(timezone.now()))[:-13],
                              user, processed, tweet_count))
            sys.stdout.flush()
        print format("%s (Twitter|%s) %i/%i          " % (
            str(timezone.localtime(timezone.now()))[:-13], user, processed,
            tweet_count))


def explore(tweet_number):
    """ (str, str, str, str) -> None
    Connects to accounts, keyword and site database, crawls within monitoring
    sites,then pushes articles which matches the keywords or foreign sites to
    the tweet database

    Keyword arguments:
    tweet_db            -- Tweet database name
    """

    # Connects to Site Database

    referring_sites = []
    rsites = ReferringSite.objects.all()
    # Retrieve, store, and print monitoring site information
    for site in rsites:
        # referring_sites is now in form [['Name', 'URL'], ...]
        referring_sites.append([site.name, site.url])

    source_sites = []
    # Retrieve, store, and print foreign site information
    ssites = SourceSite.objects.all()
    for site in ssites:
        # source_sites is now in form ['URL', ...]
        source_sites.append(site.url)

    # Retrieve all stored keywords
    keywords = ExplorerKeyword.objects.all()
    keyword_list = []

    for key in keywords:
        keyword_list.append(str(key.name))

    # Retrieve all stored Accounts
    accounts = ReferringTwitter.objects.all()
    accounts_list = []

    for account in accounts:
        accounts_list.append(str(account.name))

    source_twitter_list = []
    twitter_accounts = ExplorerSourceTwitter.objects.all()
    for key in twitter_accounts:
        source_twitter_list.append(str(key.name))

    parse_tweets(accounts_list, keyword_list, source_sites, tweet_number,source_twitter_list)


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
            print('Stopping Explorer...')
            comm_write('SS %s' % os.getpid())
            sys.exit(0)
        elif command == 'P':
            print('Pausing ...')
            comm_write('PP %s' % os.getpid())
            while comm_read()[1] == 'P':
                print('Waiting %i seconds ...' % config['sleep_time'])
                time.sleep(config['sleep_time'])
            check_command()
        elif command == 'R':
            print('Resuming ...')
            comm_write('RR %s' % os.getpid())

if __name__ == '__main__':
    # Initialize Communication Stream
    comm_init()
    config = configuration()['twitter']

    fs = config['from_start']

    while True:
        # Check for any new command on communication stream
        check_command()

        start = timeit.default_timer()

        if fs:
            explore(config['initial_tweet_count'])
            fs = False
        else:
            explore(config['iteration_tweet_count'])

        end = timeit.default_timer()
        delta_time = end - start
    sleep_time = max(config['min_iteration_time'] - delta_time, 0)
    for i in range(int(sleep_time // 5)):
        time.sleep(5)
        check_command()

    check_command()
