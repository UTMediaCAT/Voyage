from django.db import models
from Frontend.fields import URLProtocolField

# Create your models here.

class Tweet(models.Model):

    class Meta:
        verbose_name = "Referring Tweet"

    tweet_id = models.CharField(max_length=200)
    # some tweet can be more than 400 characters long
    text = models.CharField(max_length=450, default='')
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)

    def __unicode__(self):
        return self.tweet_id


class SourceSite(models.Model):
    tweet = models.ForeignKey(Tweet)
    url = models.CharField(max_length=2000)
    domain = URLProtocolField(max_length=2000, verbose_name="Source Site")
    matched = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

class SourceTwitter(models.Model):
    tweet = models.ForeignKey(Tweet)
    name = models.CharField(max_length=200)
    matched = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class CountLog(models.Model):
    tweet = models.ForeignKey(Tweet)
    retweet_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField('Date Added', blank=True, null=True)

    def __unicode__(self):
        return self.date.strftime('%Y-%m-%d')

class Keyword(models.Model):
    tweet = models.ForeignKey(Tweet)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
