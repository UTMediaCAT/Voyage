from django.db import models

# Create your models here.

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=200)
    text = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)

    def __unicode__(self):
        return self.tweet_id


class Source(models.Model):
    tweet = models.ForeignKey(Tweet)
    url = models.CharField(max_length=2000)
    domain = models.URLField(max_length=2000, verbose_name="Source Site")

    def __unicode__(self):
        return self.url

class Keyword(models.Model):
    tweet = models.ForeignKey(Tweet)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.keyword
