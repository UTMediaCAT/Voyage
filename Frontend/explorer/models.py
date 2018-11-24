from django.db import models
from django.core.exceptions import ValidationError
import tweepy, os, yaml, newspaper
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
import common
from Frontend.fields import URLProtocolField

def authorize():
    """ (None) -> tweepy.API
    Will use global keys to allow use of API
    """
    #Get's config settings for twitter
    config = common.get_config()['twitter']
    #Authorizing use with twitter development api
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    return tweepy.API(auth)

def validate_user(user):
    try:
        authorize().get_user(user)
    except:
        raise ValidationError('%s is not a valid Twitter Account!' % user)

def validate_site(site):
    try:
        s = newspaper.build(site, memoize_articles=False,
                            keep_article_html=True,
                            fetch_images=False,
                            language='en')
        if s.size() == 0:
            raise ValidationError('%s is not a valid Referring Site!' % site)
    except:
        raise ValidationError('%s is not a valid Referring Site!' % site)


# Create your models here.

class ReferringSite(models.Model):
    url = URLProtocolField(max_length=2000, unique=True, #validators=[validate_site],
                          help_text='Choose a simple URL to maximize matches. Maximum 2000 characters (Ex. http://cnn.com)')
    name = models.CharField(max_length=200, unique=True,
                            help_text='Your favorable name of this site.\n' +
                                      'Maximum 200 characters')
    # check = models.BooleanField(default=False, verbose_name="Test Newspaper RSS Scan",
    #                             help_text=mark_safe('Check to display the amount of articles found by Newspaper RSS Scan (Displays as error).<br>Uncheck to save without testing Newspaper.'))

    is_shallow =  models.BooleanField(default=False, verbose_name="Shallow State", help_text=mark_safe('Use shallow crawler to search only until depth of 5'))
    tags = TaggableManager()

    crawl_choices = (
	(0, 'RSS'),
	(1, 'MediaCAT Crawler'),
	(2, 'Both')
    )

    # crawl_count = models.IntegerField(default=0)
    mode = models.PositiveIntegerField(default=0,
		        choices=crawl_choices,
			verbose_name='Scanner',
                        help_text=mark_safe('RSS - Fast but may not work on some sites.<br>' + # Use Check Newspaper to determine the compatibility<br>' +
                                            'MediaCAT Crawler - Slow but compatible with any sites.<br>' +
                                            'Both - Uses both Newspaper and MediaCAT CrawlerB for maximum results.'))
    class Meta:
        verbose_name = 'Referring Site'

    def __str__(self):
        return self.name


class ReferringSiteFilter(models.Model):
    site = models.ForeignKey(ReferringSite)
    pattern = models.CharField(max_length=1000, help_text='Any URL that matches the pattern will be ignored from the crawler.')
    regex = models.BooleanField(default=False, help_text='Use Regular Expression instead of string comparison.')

    class Meta:
        verbose_name = "Filter"


class ReferringSiteCssSelector(models.Model):
    site = models.ForeignKey(ReferringSite)
    field_choice = (
        (0, 'Title'),
        (1, 'Author'),
        (2, 'Date Published'),
        (3, 'Date Modified')
    )
    field = models.PositiveSmallIntegerField(default=0,
                        choices=field_choice,
                        verbose_name='Field')
    pattern = models.CharField(max_length=1000, help_text='CSS Selector pattern')
    regex = models.CharField(max_length=1000, blank=True, help_text='Regular expression to further narrow down')

    class Meta:
        verbose_name = "CSS Selector"


class ReferringTwitter(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[validate_user],
                            help_text='Do not include "@". Maximum 15 characters (Ex. CNN)')
    tweets_visited = models.PositiveIntegerField(default=0)
    timeline_tweets = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Referring Twitter Account'

    def __str__(self):
        return self.name


class ReferringTwitterIgnoreURL(models.Model):
    user = models.ForeignKey(ReferringTwitter) 
    ignore_url = URLProtocolField(max_length=2000, unique=False, null=True, 
                          help_text='Choose a simple URL to help for matching. Maximum 2000 characters (Ex. http://cnn.com)')

    class Meta:
        verbose_name = 'URL To Ignore'
        verbose_name_plural = 'URLs To Ignore'

    def __str__(self):
        return self.ignore_url



class ReferringTwitterHashtag(models.Model):
    user = models.ForeignKey(ReferringTwitter)
    text = models.CharField(max_length=200)
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Hashtag'

    def __str__(self):
        return self.text


class ReferringTwitterMention(models.Model):
    user = models.ForeignKey(ReferringTwitter)
    screen_name = models.CharField(max_length=200)
    count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Mentioned User'

    def __str__(self):
        return self.screen_name



class SourceTwitter(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[validate_user],
                            help_text='Do not include "@". Maximum 15 characters (Ex. CNN)')
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Source Twitter Account'

    def __str__(self):
        return self.name


class SourceTwitterAlias(models.Model):
    primary = models.ForeignKey(SourceTwitter)
    alias = models.CharField(max_length=200, unique=True, validators=[validate_user],
                            help_text='Do not include "@". Maximum 15 characters (Ex. CNN)')

    class Meta:
        verbose_name = "Alias"
        verbose_name_plural = "Aliases"

    def __str__(self):
        return self.alias


class SourceSite(models.Model):
    url = URLProtocolField(max_length=2000, unique=True,
                          help_text='Choose a simple URL to maximize matches. Maximum 2000 characters (Ex. http://aljazeera.com)')
    name = models.CharField(max_length=200, unique=True,
                            help_text='Your favorable name of this site.')
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Source Site'

    def __str__(self):
        return self.name


class SourceSiteAlias(models.Model):
    primary = models.ForeignKey(SourceSite)
    alias = models.CharField(max_length=200, unique=True,
                            help_text='Case insensitive. Maximum 200 characters (Ex. Canada)')

    class Meta:
        verbose_name = "Alias"
        verbose_name_plural = "Aliases"

    def __str__(self):
        return self.alias


class Keyword(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            help_text='Case insensitive. Maximum 200 characters (Ex. Canada)')
    tags = TaggableManager()

    def __str__(self):
        return self.name
