from django.db import models

# Create your models here.

class Article(models.Model):
    url = models.URLField(max_length=2000)
    domain = models.URLField(max_length=2000, verbose_name="Referring Site")
    title = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)

    def __unicode__(self):
        if len(self.title) >= 30:
            return self.title[:27] + '...'
        return self.title


class Author(models.Model):
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.author 

class Source(models.Model):
    article = models.ForeignKey(Article)
    url = models.CharField(max_length=2000)
    domain = models.URLField(max_length=2000, verbose_name="Source Site")

    def __unicode__(self):
        return self.url

class Keyword(models.Model):
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.keyword
