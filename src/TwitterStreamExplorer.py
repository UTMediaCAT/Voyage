import tweepy
import time
import re
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
from tweets.models import SourceTwitter as TwitterSourceTwitter
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceTwitter as ExplorerSourceTwitter
from explorer.models import Keyword as ExplorerKeyword
import tld
# To store the article as warc files
import warc_creator
# For getting real url for get_source_sites
import requests
import collections
import common


def configuration():
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
    return auth

class ExplorerStreamListener(tweepy.StreamListener):
    def loadSearchParameters(self):
        self.sourceSiteDomains = set()
        for site in SourceSite.objects.all():
            self.sourceSiteDomains.add(tld.get_tld(site.url))

        Keyword = collections.namedtuple("Keyword", ["name", "regex"])
        self.keywords = []
        for keyword in ExplorerKeyword.objects.all():
            self.keywords.append(Keyword(keyword.name, re.compile('[^a-z]' + keyword.name + '[^a-z]', re.IGNORECASE)))

        self.sourceTwitter = set()
        for s in ExplorerSourceTwitter.objects.all():
            self.sourceTwitter.add(s.name)

    def on_status(self, status):
        try:
            print status.text
            tweet_keywords = self.get_keywords(status.text)
            (tweet_matched_urls, tweet_unmatched_urls) = self.get_source_sites(status.entities['urls'])
            (tweet_matched_accounts, tweet_unmatched_accounts) = self.get_sources_twitter(status.text)

            if tweet_keywords or tweet_matched_urls or tweet_matched_accounts:

                tweet_text = status.text
                tweet_id = status.id
                tweet_date = timezone.localtime( timezone.make_aware(status.created_at, timezone=timezone.get_fixed_timezone(180)))
                tweet_author = status.user.screen_name

                tweet_reply_to_user = status.in_reply_to_screen_name or ""
                tweet_reply_to_tweet = status.in_reply_to_status_id_str or ""
                tweet_client = status.source or ""
                tweet_filter_level = status.filter_level

                db_status = Tweet(tweet_id=tweet_id, name=tweet_author,
                                      date_added=timezone.localtime(timezone.now()),
                                      date_published=tweet_date,
                                      text=tweet_text, reply_to_user=tweet_reply_to_user, reply_to_tweet=tweet_reply_to_tweet,
                                  client=tweet_client, filter_level=tweet_filter_level)
                db_status.save()

                db_status = Tweet.objects.get(tweet_id=tweet_id)


                if("media" in status.entities):
                    media = status.entities["media"]
                    for m in media:
                        display_url = m["expanded_url"]
                        direct_url = m["media_url_https"]
                        type = m["type"]

                        #from https://gist.github.com/zed/c2168b9c52b032b5fb7d
                        import posixpath
                        from urlparse import urlsplit
                        from urllib import unquote
                        def url2filename(url):
                            '''
                            Return basename corresponding to url.
                            >>> print(url2filename('http://example.com/path/to/file%C3%80?opt=1'))
                            file
                            >>> print(url2filename('http://example.com/slash%2fname')) # '/' in name
                            Traceback (most recent call last):
                            ...
                            ValueError
                            '''
                            urlpath = urlsplit(url).path
                            basename = posixpath.basename(unquote(urlpath))
                            if (os.path.basename(basename) != basename or
                                unquote(posixpath.basename(urlpath)) != basename):
                                raise ValueError  # reject '%2f' or 'dir%5Cbasename.ext' on Windows
                            return basename
                        file_name = url2filename(direct_url)
                        save_to = os.path.join(common.get_config()["twitter"]["media_dir"], file_name)

                        req = requests.get(direct_url, stream=True)
                        with open(save_to, 'wb') as f:
                            for chunk in req.iter_content(chunk_size=4096):
                                f.write(chunk)
                        req.close()
                        db_status.tweetmedia_set.create(file_name=file_name, display_url=display_url, type=type)


                #works better than matching manually
                if("urls" in status.entities):
                    urls = status.entities["urls"]
                    for u in urls:
                        url = u["expanded_url"]
                        (text_start, text_end) = u["indices"]

                if("user_mentions" in status.entities):
                    mentions = status.entities["user_mentions"]
                    for m in mentions:
                        name = m["name"]
                        id = m["id_str"]
                        (text_start, text_end) = m["indices"]


                for account in tweet_matched_accounts:
                    db_status.sourcetwitter_set.create(name = account, matched = True)

                for account in tweet_unmatched_accounts:
                    db_status.sourcetwitter_set.create(name = account, matched = False)

                for key in tweet_keywords:
                    db_status.keyword_set.create(name=key)

                for source in tweet_matched_urls:
                    db_status.sourcesite_set.create(url=source[0], domain=source[1], matched = True)
                for source in tweet_unmatched_urls:
                    db_status.sourcesite_set.create(url=source[0], domain=source[1], matched = False)
        except Exception as e:
            print(e)


    def on_error(self, status_code):
        print(status_code)

    def get_keywords(self, text):
        matched_keywords = []
        # Searches if keyword is in tweet regardless of casing
        for k in self.keywords:
            if k.regex.search(text.encode('utf8')):
                matched_keywords.append(k.name)
        return matched_keywords


    def get_source_sites(self, urls):
        result_urls_matched = []
        result_urls_unmatched = []
        for url in urls:
            try:
                real_url = requests.get(url['expanded_url'], timeout=10).url
                domain = tld.get_tld(real_url)
            except:
                continue
            if domain in self.sourceSiteDomains:
                result_urls_matched.append((real_url, domain))
            else:
                result_urls_unmatched.append((real_url, domain))

        # Return the list
        return (result_urls_matched, result_urls_unmatched)

    def get_sources_twitter(self, tweet_text):
        matched = []
        unmatched = []
        # Twitter handle name specifications
        accounts = re.findall('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', tweet_text)

        for account in set(accounts):
            if account in self.sourceTwitter:
                matched.append(account)
            else:
                unmatched.append(account)
        return (matched,unmatched)

if __name__ == "__main__":
    django.setup()

    auth = authorize()
    api = tweepy.API(auth)

    followList = []
    for account in ReferringTwitter.objects.all():
        user = api.get_user(account.name)
        followList.append(user.id_str)

    l = ExplorerStreamListener()
    l.loadSearchParameters()

    stream = tweepy.Stream(auth=auth, listener=l)
    stream.filter(follow=followList)
