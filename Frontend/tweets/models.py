from django.db import models

# Create your models here.

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=200)
    text = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)

    reply_to_user = models.CharField(max_length=32, default='')
    reply_to_tweet = models.CharField(max_length=64, default='')
    client = models.CharField(max_length=256, default='')
    filter_level = models.CharField(max_length=16, default='')

    def __unicode__(self):
        return self.tweet_id


class SourceSite(models.Model):
    tweet = models.ForeignKey(Tweet)
    url = models.CharField(max_length=2000)
    domain = models.URLField(max_length=2000, verbose_name="Source Site")
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

class TweetMedia(models.Model):
    tweet = models.ForeignKey(Tweet)
    file_name = models.CharField(max_length=2000)
    display_url = models.CharField(max_length=2000)
    type = models.CharField(max_length=200)