from django.db import models
from django.core.exceptions import ValidationError
import tweepy, os, yaml, newspaper


def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../',"config.yaml")), 'r')
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
    url = models.URLField(max_length=2000, unique=True, validators=[validate_site],
                          help_text='Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)')
    name = models.CharField(max_length=200, 
                            help_text='Your favorable alias of this site.\n' +
                                      'Maximum 200 characters')
    
    class Meta:
        verbose_name = 'Referring Site'


    def __unicode__(self):
        return self.name


class TwitterAccount(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[validate_user],
                            help_text='Do not include "@". Maximum 15 characters (Ex. CNN)')
    class Meta:
        verbose_name = 'Twitter Account'

    def __unicode__(self):
        return self.account


class SourceSite(models.Model):
    url = models.URLField(max_length=2000, unique=True, 
                          help_text='Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://aljazeera.com)')
    name = models.CharField(max_length=200, 
                            help_text='Your favorable alias of this site.')
    class Meta:
        verbose_name = 'Source Site'

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=200, unique=True, 
                            help_text='Case insensitive. Maximum 200 characters (Ex. Canada)')
    
    def __unicode__(self):
        return self.keyword

