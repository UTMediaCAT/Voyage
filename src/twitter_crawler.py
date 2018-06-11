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
                real_url = requests.get(url, timeout=10).url
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
        try:
            if re.search('[^a-z]' + key + '[^a-z]', text.encode('utf8'), re.IGNORECASE):
                matched_keywords.append(key)
        except Exception as e:
            print(e)
    return matched_keywords


def get_source_twitter(mentioned_user, source_twitter):
    """ (Dict, list of source twitter screen name)
        - > [list of matched twitter, list of unmatched twitter]
    Search for mentioned twitter screen name in the tweet.
    """
    matched = []
    unmatched = []
    # get a list of mentioned user screen names
    # mentioned_users = [str(mention['screen_name']) for mention in tweet['entities']['user_mentions']]

    # check if mentioned user is in scope's Source Twitter Accounts 
    for user in mentioned_user:
        if user in source_twitter:
            matched.append(user)
        else:
            unmatched.append(user)
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


def convert_datetime_from_csv(date):
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
    return timezone.localtime(timezone.make_aware(dt,
                              timezone=timezone.get_fixed_timezone(0)))


def get_source_site_from_csv(tweet_text):
    """
    Return urls in given tweet text crawled by GetOldTweets-python
    """
    tweet_text = tweet_text.replace(ur"\u2026", "\n")
    try: 
        urls = {str(url.replace(" ", "")) for url in re.findall("https?:\/\/.*html", tweet_text)}
        urls.update({str(url.replace(" ", "")[:-1]) for url in re.findall("https?:\/\/ ?\S*\"", tweet_text)})
        urls.update({str(url.replace(" ", "")) for url in re.findall("(https?:\/\/.*?)\n", tweet_text)})
    except:
        urls = set()
    return list(urls)


class Crawler_Tweet(object):
    """Tweet object which stores tweet relating information"""
    def __init__(self, user, text, tweet_id, date, urls, mentions, retweet_count, favorite_count):
        self.user, self.text, self.tweet_id, self.date, self.urls, self.mentions, self.retweet_count, self.favorite_count = user, text, tweet_id, date, urls, mentions, retweet_count, favorite_count


def build_Tweet_from_csv(tweet):
    """ 
    Build Tweet object based on tweet crawled by GetOldTweets-python.
    """
    info = tweet.split(";")
    if (len(info) != 10):
        return None
    else:
        tweet_user = info[0]
        tweet_text = info[4]
        tweet_id = info[8].strip("\"")
        tweet_date = convert_datetime_from_csv(info[1])
        urls = get_source_site_from_csv(tweet_text)
        mentions = [mention[1:] for mention in info[6].split()]
        retweet_count = info[2]
        favorite_count = info[3]
        return Crawler_Tweet(tweet_user, tweet_text, tweet_id, tweet_date, urls, mentions, retweet_count, favorite_count)


def process_tweet(tweet, keywords, source_sites, source_accounts):
    """
    Checks if the given tweet match the scope.
    """
    user, tweet_text, tweet_id, tweet_date = tweet.user, tweet.text, tweet.tweet_id, tweet.date
    tweet_store_date = timezone.localtime(timezone.now())    
    tweet_keywords = get_keywords(tweet_text, keywords)
    tweet_sources = get_source_sites(tweet.urls, source_sites)
    twitter_accounts = get_source_twitter(tweet.mentions, source_accounts)
    retweet_count, favorite_count = tweet.retweet_count, tweet.favorite_count

    if len(tweet_text) > 450:
        try:
            tweet_text = tweet_text[:450]
        except:
            return NO_MATCH

    # finds match
    if tweet_keywords or tweet_sources[0] or twitter_accounts[0]:
        existing_tweets = Tweet.objects.filter(tweet_id=tweet_id)

        if not existing_tweets:
            tweet = Tweet(tweet_id=tweet_id,
                        name=user,
                        date_added=tweet_store_date,
                        date_published=tweet_date,
                        text=tweet_text)
            tweet.save()
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
            try:
                warc_creator.create_twitter_warc(
                    'https://twitter.com/' + tweet.name + '/status/' +str(tweet_id))
                # adjustable, give time for warc creation and avoids using too many resources
                time.sleep(3)
            except:
                print("Warc error at {}.{}".format(user, tweet_id))
                logging.error("Warc error at {}.{}".format(user, tweet_id))

            return ADDED

        else:
            tweet = existing_tweets[0]
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
                    tweet.sourcesite_set.create(
                        url=source[0], domain=source[1], matched=False)

            for account in twitter_accounts[0]:
                if not tweet.sourcetwitter_set.filter(name=account):
                    tweet.sourcetwitter_set.create(name=account, matched=True)

            for account in twitter_accounts[1]:
                if not tweet.sourcetwitter_set.filter(name=account):
                    tweet.sourcetwitter_set.create(name=account, matched=False)
            return UPDATED
    return NO_MATCH


def lines_of_file(file_path):
    """ 
    Return the number of lines in the file specified by the given path
    """
    with open(file_path) as f:
        lines = sum(1 for _ in f)
    return lines


def process_history(screen_name):
    """
    Process the crawled tweets of the given user from the csv file
    """
    config = common.get_config()
    log_dir = config['projectdir']+"/log"

    source_sites = [site.url for site in SourceSite.objects.all()]
    # get the key words in scope
    keyword_list = [str(key.name) for key in ExplorerKeyword.objects.all()]
    # Retrieve all source twitter accounts in the scope
    source_accounts = [str(account.name) for account in ExplorerSourceTwitter.objects.all()]

    added, updated, no_match = 0, 0, 0

    user = ReferringTwitter.objects.filter(name=screen_name)[0]
    # ignore URLs speficied for this user
    temp_source_sites = ignore_url(user, source_sites)
    processed = 0
    csv_path = "{}/tweet_csv/{}.csv".format(log_dir, user)
    tweet_count = lines_of_file(csv_path) - 1
    with open(csv_path, "r") as tweet_csv:
        for tweet in tweet_csv:
            print("processing {}".format(tweet))
            tweet = tweet.decode('utf-8').strip()
            if processed == 0:
                # skip first line of csv file
                processed += 1
                continue
            processed += 1
            tweet_obj = build_Tweet_from_csv(tweet)
            if tweet_obj:
                process_result = process_tweet(tweet_obj, keyword_list, temp_source_sites, source_accounts)
            else:
                continue
            if process_result == ADDED:
                added += 1
            elif process_result == UPDATED:
                updated += 1
            else:
                no_match += 1

            # update total tweets visited
            user.tweets_visited = user.tweets_visited + 1
            user.save()
            logging.info("{} (History|{}) {}/{}          \r".format(
                             str(timezone.localtime(timezone.now()))[:-13],
                              user.name, processed, tweet_count))


def build_Tweet_from_Twarc_tweet(tweet):
    tweet_user = get_tweet_user(tweet)
    tweet_text = get_tweet_text(tweet)
    tweet_id = get_twitter_id(tweet)
    tweet_date = get_tweet_date(tweet)
    tweet_urls = [url['expanded_url'] for url in tweet['entities']['urls']]
    tweet_mentions = [str(mention['screen_name']) for mention in tweet['entities']['user_mentions']]
    retweet_count = get_retweet_count(tweet)
    favorite_count = get_favorites_count(tweet)
    return Crawler_Tweet(tweet_user, tweet_text, tweet_id, tweet_date, tweet_urls, tweet_mentions, retweet_count, favorite_count)


def update_hashtag(tweet, hashtags):
    """ (Tweet, dict) -> list of hashtags
    Update the hashtags count according to the given Tweet object.
    Return a list of hashtags in the given Tweet
    """
    hashtags_found = [t['text'] for t in tweet['entities']['hashtags']]
    for ht in hashtags_found:
        if ht in hashtags:
            hashtags[ht] += 1
        else:
            hashtags[ht] = 1
    return hashtags_found


def update_mention(tweet, mentions):
    """ (Tweet, dict) -> list
    Return a list of mentioned twitter acccount in the given twitter object. 
    Update the given count of mentioned twitter account in the given dictionary.  
    """
    mentioned_users = [str(mention['screen_name']) for mention in tweet['entities']['user_mentions']]
    for user in mentioned_users:
        if user in mentions:
            mentions[user] += 1
        else:
            mentions[user] = 1
    return mentioned_users


def ignore_url(user, source_sites):
    """ (str, list) -> list
    Return a list of source sites of the given user with ignored URLs removed. 
    """
    urls_to_ignore = [get_tld(str(url)) for url in ReferringTwitterIgnoreURL.objects.filter(user=user)]
    return [url for url in source_sites if get_tld(url) not in urls_to_ignore]


def parse_tweet(users, source_sites, keywords, source_accounts):
    """
    Crawls timeline tweets from give list of users.
    """
    added, updated, no_match = 0, 0, 0
    # start = time.time()

    # Parse each user's timeline 
    for account in users:
        user = str(account.name)
        hashtags = {}
        mentions = {}

        # remove current user's ignored urls from source sites 
        temp_source_sites = ignore_url(account, source_sites)
        processed = 0
        # get user info
        twarc_user = auth.user_lookup([user], "screen_name").next()
        tweets = get_tweets(user)
        followers_count = get_follower_count(twarc_user)
        tweet_count = len(tweets)   

        # update timeline tweets count
        account.timeline_tweets = tweet_count
        account.save()

        for i in range(tweet_count):
            tweet = tweets[i]
            hashtag_list = update_hashtag(tweet, hashtags)
            if hashtag_list:
                logging.info("{} (Timeline|{}) {}/{} hashtags: {}          \r".format(
                         str(timezone.localtime(timezone.now()))[:-13],
                          user, i, tweet_count, ",".join(hashtag_list).encode('utf-8')))
            mentioned_users = update_mention(tweet, mentions)
            if mentioned_users:
                logging.info("{} (Timeline|{}) {}/{} mentions: {}          \r".format(
                             str(timezone.localtime(timezone.now()))[:-13],
                              user, i, tweet_count, ",".join(mentioned_users).encode('utf-8')))
            process_result = process_tweet(build_Tweet_from_Twarc_tweet(tweet), keywords, temp_source_sites, source_accounts)
            if process_result == ADDED:
                added += 1
            elif process_result == UPDATED:
                updated += 1
            else:
                no_match += 1
            processed += 1

            logging.info("{} (Timeline|{}) {}/{}          \r".format(
                             str(timezone.localtime(timezone.now()))[:-13],
                              user, processed, tweet_count))

        print format("%s (Timeline|%s) %i/%i          " % (
            str(timezone.localtime(timezone.now()))[:-13], user, processed,
            tweet_count))

        ReferringTwitterHashtag.objects.filter(user=account).delete()
        for ht in hashtags:
            print(u"{}: {}".format(ht, hashtags[ht]))
            logging.info(u"{}: {}".format(ht, hashtags[ht]))
            hashtag = ReferringTwitterHashtag(user=account, text=ht, count=hashtags[ht])
            hashtag.save()

        ReferringTwitterMention.objects.filter(user=account).delete()
        for mentioned_user, count in mentions.items():
            print(u"{}: {}".format(mentioned_user, count))
            logging.info(u"{}: {}".format(mentioned_user, count))
            new_mention = ReferringTwitterMention(user=account, screen_name=mentioned_user, count=count)
            new_mention.save()


def get_history_csv(user):
    """
    Get all tweets of the given user and store them into a csv file.
    """
    config = common.get_config()
    log_dir = config['projectdir']+"/log"
    exporter_path = "GetOldTweets-python/Exporter.py"
    output_path = "{}/tweet_csv/{}.csv".format(log_dir, user)
    log_path = "{}/get_history_{}.log".format(log_dir, user)
    print("Getting tweet history of {}".format(user))
    with open(log_path, "w") as outfile:
        subprocess.call(["python", exporter_path, "--username", "\"{}\"".format(user),
            "--output", output_path], stdout=outfile)


def get_user_id(screen_name):
    """ (list of str)-> list of int
    Return the twitter users' ids given a list of their screen names.
    """
    users = auth.user_lookup(screen_name, "screen_name")
    ids = []
    for user in users:
        ids.append(user['id'])
    return ids


def explore():
    # get the source site url in scope
    source_sites = [site.url for site in SourceSite.objects.all()]
    # get the key words in scope
    keyword_list = [str(key.name) for key in ExplorerKeyword.objects.all()]
    # Retrieve all referring twitter accounts (to be explored)
    referring_accounts = list(ReferringTwitter.objects.all())
    # Retrieve all source twitter accounts in the scope
    source_accounts = [str(account.name) for account in ExplorerSourceTwitter.objects.all()]

    parse_tweet(referring_accounts, source_sites, keyword_list, source_accounts)


def streaming():
    """
    Crawl realtime tweets
    """
    source_sites = [site.url for site in SourceSite.objects.all()]
    # get the key words in scope
    keyword_list = [str(key.name) for key in ExplorerKeyword.objects.all()]
    # Retrieve all referring twitter accounts (to be explored)
    referring_accounts = [str(account.name) for account in ReferringTwitter.objects.all()]
    # Retrieve all source twitter accounts in the scope
    source_accounts = [str(account.name) for account in ExplorerSourceTwitter.objects.all()]
    # get lower case user screen names for case-insensitive checking
    ids = get_user_id(referring_accounts)
    lowercase_users = [screen_name.lower() for screen_name in referring_accounts]

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
        if user.lower() in lowercase_users:
            tweet_id = get_twitter_id(tweet)
            referring_twitter = ReferringTwitter.objects.filter(name__iexact=user)[0]
            temp_source_sites = ignore_url(referring_twitter, source_sites)
            result = process_tweet(build_Tweet_from_Twarc_tweet(tweet), keyword_list, temp_source_sites, source_accounts)
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
            logging.info(status_report)
            # update total tweets visited
            referring_twitter.tweets_visited = referring_twitter.tweets_visited + 1
            referring_twitter.save()
        else:
            status_report = "{} (Streaming|{}) -- Screen name: {}, not a referring user".format(str(timezone.localtime(timezone.now()))[:-13], 
                count, user)
            logging.info(status_report)


def history():
    """
    Crawls all history tweet for referring twitter accounts in scope using GetOldTweets
    """
    processes = []
    users = [str(account.name) for account in ReferringTwitter.objects.all()]

    # crawls history of all users
    for user in users:
        processes.append(subprocess.Popen(["python", "./twitter_crawler.py", "history", user]))

    # wait for all crawling to finish to start processing
    # so that history crawling does not take too much resource
    for p in processes:
        p.wait()

    # proceess one user at a time, does taking up too much memory
    for user in users:
        process_history(user)


def setup_logging(name):
    """
    Set up the logging file.
    Modified from setup_logging from article_explorer.py
    """
    config = common.get_config()
    # Logging config
    current_time = datetime.now().strftime('%Y%m%d')
    log_dir = config['projectdir']+"/log"
    prefix = log_dir + "/" + name + "-twitter_crawler-"

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
        if sys.argv[1] not in ("streaming", "timeline", "history"):
            print("Invalid arguments {}".format(" ".join(sys.argv[1:])))
        else:
            auth = authorize()
            if sys.argv[1] == "history":
                if len(sys.argv) > 2:
                    setup_logging("history_crawling_{}".format(sys.argv[2]))
                    get_history_csv(sys.argv[2])
                    logging.info("Crawled history of {}".format(sys.argv[2]))
                else: 
                    setup_logging("history")
                    history()
                    logging.info("Done history")
                    # crawline timeline
            else:
                # create log files with name matching given option
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
                        setup_logging("timeline")
                        time.sleep(60*60*24)
    else:
        # will do both streaming, timeline and history crawling if no arguments are given
        subprocess.Popen(["python", "./twitter_crawler.py", "streaming"])
        subprocess.Popen(["python", "./twitter_crawler.py", "timeline"])
        subprocess.call(["python", "./twitter_crawler.py", "history"])

