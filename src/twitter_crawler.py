import time
# for converting tweeter time to django time
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import re
from tld import get_tld
from tld.utils import update_tld_names
import timeit
import sys
import os
import django
import yaml
from twarc import Twarc
import logging
import subprocess
# for setting proper logging file name
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'

import requests
# For timing out the requests properly
import eventlet
eventlet.monkey_patch()

# For getting today's date
from django.utils import timezone

from tweets.models import*
from tweets.models import Keyword as TwitterKeyword
from tweets.models import SourceSite as TwitterSourceSite
from tweets.models import SourceTwitter as TwitterSourceTwitter
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceTwitter as ExplorerSourceTwitter
from explorer.models import Keyword as ExplorerKeyword
# For getting real url for get_source_sites
import tld
# To store the article as warc files
import warc_creator

# setting up database
django.setup()

ADDED = 0
UPDATED = 1
NO_MATCH = 2

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
    """
    Return authorized Twarc handler with the credentials stored in config file.
    """
    config = configuration()['twitter']
    twarc_auth = Twarc(config['consumer_key'], config['consumer_secret'],
                       config['access_token'], config['access_token_secret'])
    return twarc_auth


def to_datetime(datestring):
    """
    Return datetime format given twitter date format.
    """
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])


def get_tweet_date(tweet):
    """
    Return the django date of the given tweet's created time.
    """
    dt = to_datetime(tweet['created_at'])
    return timezone.localtime(timezone.make_aware(dt,
                              timezone=timezone.get_fixed_timezone(0)))


def get_tweet_user(tweet):
    """
    Return the creator's screen name of the given tweet.
    """
    return str(tweet['user']['screen_name'])


def get_tweets(screen_name):
    """
    Returns the most recent 3200 (or all if < 3200 available) tweets of
    the given user specified by twitter screen name
    """
    tweets = []
    for tweet in auth.timeline(screen_name=screen_name):
        tweets.append(tweet)
    return tweets


def get_retweet_count(tweet):
    return tweet['retweet_count']


def get_favorites_count(tweet):
    return tweet['favorite_count']


# modified from twitter_explorer.py
def get_source_sites(urls, sites):
    """ (list of urls, list of source site urls)
    Return a list of expanded urls found in source urls,
    and a list of expanded urls not found in srouce urls.
    """
    result_urls_matched = []
    result_urls_unmatched = []
    formatted_source_sites = []
    for site in sites:
        formatted_source_sites.append(tld.get_tld(site))
    for url in urls:
        try:
            # with eventlet, the request will time out in 10s
            with eventlet.Timeout(10):
                real_url = requests.get(url['expanded_url'], timeout=10).url
            domain = tld.get_tld(real_url)
        except:
            continue
        if domain in formatted_source_sites:
            # If it matches even once, append the site to the list
            result_urls_matched.append([real_url, domain])
        else:
            result_urls_unmatched.append([real_url, domain])

    return [result_urls_matched,result_urls_unmatched]


def get_follower_count_from_tweet(tweet):
    """
    Return the number of followers of the poster of the given tweet.
    """
    return tweet['user']['followers_count']


def get_follower_count(twarc_user):
    """
    Return the folower count of a twitter user object.
    """
    return twarc_user['followers_count']


def get_twitter_id(tweet):
    """
    Return the id of the user from a tweet object.
    """
    return tweet['id']


# From twitter_explorer.py
def get_keywords(text, keywords):
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
        if re.search('[^a-z]' + key + '[^a-z]', text.encode('utf8'), re.IGNORECASE):
            matched_keywords.append(key)
    return matched_keywords


# From twitter_explorer.py
def get_sources_twitter(tweet_text, source_twitter):
    """ (str, list of source twitter screen name)
        - > [list of matched twitter, list of unmatched twitter]
    Search for mentioned twitter screen name in the tweet.
    """
    matched = []
    unmatched = []
    # Twitter handle name specifications
    accounts = re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', tweet_text)

    for account in set(accounts):
        if account in source_twitter:
            matched.append(account)
        else:
            unmatched.append(account)
    return [matched,unmatched]


def get_tweet_text(tweet):
    """
    Return the text content of a tweet.
    """
    # timeline and streaming tweets are dealt differently
    if "full_text" in tweet:
        return tweet['full_text']
    else:
        return tweet['text']


def ddubug(id):
    print("\t {}".format(id))


def process_tweet(tweet, user, keywords, source_sites, source_accounts):
    """ 
    Process the given tweet, check if it matches any of the given scope.
    """
    ddubug(2)
    tweet_text = get_tweet_text(tweet)
    tweet_id = get_twitter_id(tweet)
    tweet_date = get_tweet_date(tweet)
    ddubug(3)
    tweet_store_date = timezone.localtime(timezone.now())
    tweet_keywords = get_keywords(tweet_text, keywords)
    tweet_sources = get_source_sites(tweet[u'entities'][u'urls'], source_sites)
    twitter_accounts = get_sources_twitter(tweet_text, source_accounts) 
    ddubug(4)
    print("Processing \t{}\t{}".format(user, tweet_id))

    # deal with tweets that are too long
    if len(tweet_text) > 300:
        f = open("too_long_tweet.log", "a")
        f.write("Tweet id: {}, length: {}\n".format(tweet_id, len(tweet_text)))
        # f.write(tweet_text)
        f.write("\n\n")
        f.flush()
        f.close()
        print("Tweet too long! {}".format(len(tweet_text)))
        print("\tTweet id: {}".format(tweet_id))
        try:
            tweet_text = tweet[:300]
        except:
            return NO_MATCH

    # finds match
    if tweet_keywords or tweet_sources[0] or twitter_accounts[0]:
        retweet_count = get_retweet_count(tweet)
        favorite_count = get_favorites_count(tweet)
        ddubug(5)

        existing_tweets = Tweet.objects.filter(tweet_id=tweet_id)

        if not existing_tweets:
            tweet = Tweet(tweet_id=tweet_id,
                        name=user,
                        date_added=tweet_store_date,
                        date_published=tweet_date,
                        text=tweet_text)
            tweet.save()
            ddubug(5)
            tweet = Tweet.objects.get(tweet_id=tweet_id)
            tweet.countlog_set.create(retweet_count = retweet_count,
                                    favorite_count = favorite_count,
                                    date =tweet_store_date)

            for account in twitter_accounts[0]:
                tweet.sourcetwitter_set.create(name=account, matched=True)
            for account in twitter_accounts[1]:
                tweet.sourcetwitter_set.create(name=account, matched=False)
            for key in tweet_keywords:
                tweet.keyword_set.create(name=key)
            for source in tweet_sources[0]:
                tweet.sourcesite_set.create(url=source[0], domain=source[1], matched=True)
            for source in tweet_sources[1]:
                tweet.sourcesite_set.create(url=source[0], domain=source[1], matched=False)
            ddubug(6)
            try:
                ddubug(7)
                warc_creator.create_twitter_warc(
                    'https://twitter.com/' + tweet.name + '/status/' +str(tweet_id))
                ddubug(8)
                # adjustable, give time for warc creation and avoids using too many resources
                time.sleep(10)
            except:
                print("Warc error at {}.{}".format(user, tweet_id))
                logging.error("Warc error at {}.{}".format(user, tweet_id))

            return ADDED

        else:
            ddubug(9)
            tweet = existing_tweets[0]
            # update tweet fields
            tweet.text = tweet_text
            tweet.tweet_id = tweet_id
            tweet.name = user
            tweet.date_published = tweet_date
            tweet.save()
            ddubug(10)
            if not tweet.countlog_set.filter(retweet_count=retweet_count, favorite_count=favorite_count):
                tweet.countlog_set.create(retweet_count=retweet_count, 
                    favorite_count=favorite_count, date=tweet_store_date)

            for key in tweet_keywords:
                if not tweet.keyword_set.filter(name=key):
                    tweet.keyword_set.create(name=key)

            for source in tweet_sources[0]:
                if not tweet.sourcesite_set.filter(url=source[0]):
                    tweet.sourcesite_set.create(
                        url=source[0], domain=source[1], matched=True)

            for source in tweet_sources[1]:
                if not tweet.sourcesite_set.filter(url=source[0]):
                    tweet.source_set.create(
                        url=source[0], domain=source[1], matched=False)

            for account in twitter_accounts[0]:
                if not tweet.sourcetwitter_set.filter(name=account):
                    tweet.sourcetwitter_set.create(name=account, matched=True)

            for account in twitter_accounts[0]:
                if not tweet.sourcetwitter_set.filter(name=account):
                    tweet.sourcetwitter_set.create(name=account, matched=False)
            ddubug(11)
            return UPDATED

    return NO_MATCH


def parse_tweet(users, source_sites, keywords, source_accounts):
    """
    Crawls timeline tweets from give list of users.
    """
    config = configuration()['storage']
    added, updated, no_match = 0, 0, 0
    start = time.time()

    # Parse each user's timeline 
    for account in users:
        user = str(account.name)

        ignore_url = str(account.ignore_url)
        temp_source_sites = [site for site in source_sites if get_tld(site) != get_tld(ignore_url)] if ignore_url else source_sites
        processed = 0
        # get user info
        twarc_user = auth.user_lookup([user], "screen_name").next()
        ddubug(1)
        tweets = get_tweets(user)
        followers_count = get_follower_count(twarc_user)
        tweet_count = len(tweets)   

        for i in range(tweet_count):
            ddubug(2)
            tweet = tweets[i]
            process_result = process_tweet(tweet, user, keywords, temp_source_sites, source_accounts)
            if process_result == ADDED:
                added += 1
            elif process_result == UPDATED:
                updated += 1
            else:
                no_match += 1
            processed += 1

            # print("%s (Twitter|%s) %i/%i          \r" %
            #                  (str(timezone.localtime(timezone.now()))[:-13],
            #                   user, processed, tweet_count))
            logging.info("%s (Twitter|%s) %i/%i          \r" %
                             (str(timezone.localtime(timezone.now()))[:-13],
                              user, processed, tweet_count))

        print format("%s (Twitter|%s) %i/%i          " % (
            str(timezone.localtime(timezone.now()))[:-13], user, processed,
            tweet_count))


def explore():
    # get the source site url in scope
    source_sites = []
    for site in SourceSite.objects.all():
        source_sites.append(site.url)

    # get the key words in scope
    keyword_list = []
    for key in ExplorerKeyword.objects.all():
        keyword_list.append(str(key.name))

    # Retrieve all referring twitter accounts (to be explored)
    # referring_accounts = ["mjplitnick"]
    referring_accounts = ReferringTwitter.objects.filter(name__icontains="Now")
    # for account in ReferringTwitter.objects.all():
    #     referring_accounts.append(str(account.name))

    # Retrieve all source twitter accounts in the scope
    source_accounts = []
    for account in ExplorerSourceTwitter.objects.all():
        source_accounts.append(str(account.name))

    parse_tweet(referring_accounts, source_sites, keyword_list, source_accounts)




def get_user_id(screen_name):
    """ list of str -> list of int
    Return the twitter users' ids given a list of their screen names.
    """
    users = auth.user_lookup(screen_name, "screen_name")
    ids = []
    for user in users:
        ids.append(user['id'])
    return ids


def streaming():
    source_sites = []
    for site in SourceSite.objects.all():
        source_sites.append(site.url)

    # get the key words in scope
    keyword_list = []
    for key in ExplorerKeyword.objects.all():
        keyword_list.append(str(key.name))

    # Retrieve all referring twitter accounts (to be explored)
    referring_accounts = []
    for account in ReferringTwitter.objects.all():
        referring_accounts.append(str(account.name))

    # Retrieve all source twitter accounts in the scope
    source_accounts = []
    for account in ExplorerSourceTwitter.objects.all():
        source_accounts.append(str(account.name))

    # get lower case user screen names for case-insensitive checking
    ids = get_user_id(referring_accounts)
    lower_case_users = [screen_name.lower() for screen_name in referring_accounts]

    count, user_tweets, added, updated, no_match = 0, 0, 0, 0, 0
    for tweet in auth.filter(follow=(",".join([str(user_id) for user_id in ids]))):
        count += 1
        # user = get_tweet_user(tweet)
        try:
            user = get_tweet_user(tweet)
        except:
            logging.debug("Cannot get user from tweet {}\n".format(tweet))
            print("Cannot get user from tweet {}\n".format(tweet))
            continue
        if user.lower() in lower_case_users:
            tweet_id = get_twitter_id(tweet)
            result = process_tweet(tweet, user, keyword_list, source_sites, source_accounts)
            if result == ADDED:
                streaming_result = "added"
                added += 1
            elif result == UPDATED:
                streaming_result = "updated"
                updated += 1
            else:
                streaming_result = "no_match"
                no_match += 1
            user_tweets += 1
            status_report = "{} Streaming ({}): \t {}/{}\t\t -- {} added: {}, updated: {}, no_match: {}, total: {}".format(
                str(timezone.localtime(timezone.now()))[:-13], 
                streaming_result, user, tweet_id, user_tweets, added, updated, no_match, count)
            print(status_report)
            logging.info(status_report)
        else:
            status_report = "{} (Streaming|{}) User: {} not found".format(str(timezone.localtime(timezone.now()))[:-13], 
                count, user)
            print(status_report)
            logging.info(status_report)

def setup_logging(name):
    """
    Set up the logging file.
    Modified from setup_logging from article_explorer.py
    """
    config = common.get_config()
    # Logging config
    current_time = datetime.now().strftime('%Y%m%d')
    log_dir = config['projectdir']+"/log"
    prefix = log_dir + "/" + name + "twitter_crawler(" + name + ")-"

    # set cycle number, starting from 0
    try:
        cycle_number = sorted(glob.glob(prefix + current_time + "*.log"))[-1][-7:-4]
        print("Found cycle number {}".format(cycle_number))
        cycle_number = str(int(cycle_number) + 1)
    except (KeyboardInterrupt, SystemExit):
        print("error")
        raise
    except:
        print("0")
        cycle_number = "0"

    # Remove all handlers associated with the root logger object.
    # This will allow logging per site
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # set up logger
    logging.basicConfig(filename=prefix + current_time + "-" + cycle_number.zfill(3) + ".log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    default_logger = logging.getLogger('')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(default_logger.handlers[0].formatter)
    default_logger.addHandler(console_handler)


if __name__ == '__main__':
    # two functionalities: timeline for history tweets and streaming for realtime tweets
    config = configuration()['twitter']
    if len(sys.argv) > 1:
        if sys.argv[1] not in ("streaming", "timeline"):
            print("Invalid arguments {}".format(" ".join(sys.argv[1:])))
        else:
            auth = authorize()
            # logging_filename = "{}_twitter_{}.log".format(sys.argv[1], datetime.now())
            # logging.basicConfig(filename=logging_filename, level=logging.INFO)
            setup_logging(sys.argv[1])
            if sys.argv[1] == "streaming":
                streaming()
            else:
                #timeline
                while True:
                    explore()
                    # re-crawl timeline every week
                    # scope change will take effect in new crawling cycle
                    logging.info("Sleep until next cycle")
                    setup_logging()
                    time.sleep(60)
    else:
        # will do both timeline and streaming if no arguments are given
        subprocess.Popen(["python", "./twitter_crawler.py", "streaming"])
        # explore()
        subprocess.Popen(["python", "./twitter_crawler.py", "timeline"])

