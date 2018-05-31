from django.db import models
from Frontend.fields import URLProtocolField
from django.conf.global_settings import LANGUAGES

# Create your models here.

class Article(models.Model):
    domain = URLProtocolField(max_length=2000, verbose_name="Referring Site")

    def __unicode__(self):
        if len(self.title) >= 30:
            return self.title[:27] + '...'
        return self.title

    @property
    def url(self):
        return self.url_set.first().name

    @property
    def title(self):
        return self.version_set.last().title

    @property
    def text(self):
        return self.version_set.last().text

    @property
    def text_hash(self):
        return self.version_set.last().text_hash

    @property
    def language(self):
        return self.version_set.last().language

    @property
    def date_added(self):
        return self.version_set.last().date_added

    @property
    def date_last_seen(self):
        return self.version_set.last().date_last_seen

    @property
    def date_published(self):
        return self.version_set.last().date_published

    @property
    def found_by(self):
        return self.version_set.last().found_by


class Url(models.Model):
    article = models.ForeignKey(Article)
    name = URLProtocolField(max_length=2000, verbose_name="URL", unique=True)

    def __unicode__(self):
        return self.name


class Version(models.Model):
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(max_length=None, blank=True)
    text_hash = models.CharField(max_length=100, blank=True, unique=True)
    language = models.CharField(max_length=200, choices=LANGUAGES, blank=True)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_last_seen = models.DateTimeField('Date Last Seen', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)
    found_by = models.CharField(max_length=100, blank=True)


    def __unicode__(self):
        return str(list(self.article.version_set.all()).index(self) + 1)

class Author(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class SourceSite(models.Model):
    version = models.ForeignKey(Version)
    url = models.CharField(max_length=2000)
    domain = URLProtocolField(max_length=2000, verbose_name="Source Site")
    anchor_text = models.CharField(max_length=2000, verbose_name="Anchor Text")
    matched = models.BooleanField(default=False)
    local = models.BooleanField(default=True)

    text = models.TextField(max_length=None, blank=True, null=True)
    text_hash = models.CharField(max_length=100, blank=True, unique=True, null=True)
    language = models.CharField(max_length=200, choices=LANGUAGES, blank=True, null=True)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_last_seen = models.DateTimeField('Date Last Seen', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)
    is_referring = models.NullBooleanField(default=None)

    def __unicode__(self):
        return self.url


class SourceTwitter(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=200)
    matched = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
