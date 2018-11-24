from django.db import models
from Frontend.fields import URLProtocolField
from django.conf.global_settings import LANGUAGES

# Create your models here.

class Article(models.Model):
    domain = URLProtocolField(max_length=2000, verbose_name="Referring Site")
    is_referring = models.NullBooleanField()
    is_source = models.NullBooleanField()
    referrals = models.ManyToManyField('self', related_name='sources', symmetrical=False)

    class Meta:
        verbose_name = "Referring Article"

    def __str__(self):
        if len(self.title) >= 30:
            return self.title[:27] + '...'
        return self.title

    @property
    def url(self):
        return self.url_set.first().name

    @property
    def title(self):
        if (self.version_set.last() == None):
            return "Version DNE"
        return self.version_set.last().title

    @property
    def text(self):
        return self.version_set.last().text

    @property
    def text_hash(self):
        return self.version_set.last().text_hash

    @property
    def language(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().language

    @property
    def date_added(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().date_added

    @property
    def date_last_seen(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().date_last_seen

    @property
    def date_published(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().date_published

    @property
    def found_by(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().found_by

    @property
    def source_url(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().sourcesite_set.last().url

    @property
    def source_anchor_text(self):
        if (self.version_set.last() == None):
            return "(None)"
        return self.version_set.last().sourcesite_set.last().anchor_text

    @property
    def source_matched(self):
        if (self.version_set.last() == None):
            return False
        return self.version_set.last().sourcesite_set.last().matched

    @property
    def source_local(self):
        if (self.version_set.last() == None):
            return False
        return self.version_set.last().sourcesite_set.last().local




class Url(models.Model):
    article = models.ForeignKey(Article)
    name = URLProtocolField(max_length=2000, verbose_name="URL", unique=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=20000, blank=True)
    text = models.TextField(max_length=None, blank=True)
    text_hash = models.CharField(max_length=20000, blank=True, unique=True)
    language = models.CharField(max_length=20000, choices=LANGUAGES, blank=True)
    date_added = models.DateTimeField('Date Added', blank=True, null=True)
    date_last_seen = models.DateTimeField('Date Last Seen', blank=True, null=True)
    date_published = models.DateTimeField('Date Published', blank=True, null=True)
    found_by = models.CharField(max_length=20000, blank=True)

    # source_url = models.CharField(max_length=2000, blank=True, null=True)
    #source_domain = URLProtocolField(max_length=2000, verbose_name="Source Site", blank=True, null=True)
    # source_anchor_text = models.CharField(max_length=2000, verbose_name="Anchor Text", blank=True, null=True)
    # source_matched = models.NullBooleanField(default=False)
    # source_local = models.NullBooleanField(default=True)


    def __str__(self):
        return str(list(self.article.version_set.all()).index(self) + 1) + self.title

# class SourceProxy(models.Model):
#     version = models.ForeignKey(Version)

#     @property
#     def url(self):
#         return self.version.source_url
    
#     @property
#     def domain(self):
#         return self.version.article.domain
    
#     @property
#     def url(self):
#         return self.version.source_url
    
#     @property
#     def anchor_text(self):
#         return self.version.source_anchor_text

#     @property
#     def matched(self):
#         return self.version.souce_matched

#     @property
#     def local(self):
#         return self.version.source_local
    


class Author(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=20000)

    def __str__(self):
        return self.name


class SourceSite(models.Model):

    class Meta:
        verbose_name = "Sourced Article"

    version = models.ForeignKey(Version)
    url = models.CharField(max_length=20000)
    domain = URLProtocolField(max_length=20000, verbose_name="Source Site")
    anchor_text = models.CharField(max_length=20000, verbose_name="Anchor Text")
    matched = models.BooleanField(default=False)
    local = models.BooleanField(default=True)
    referring_url = models.CharField(max_length=20000, default="")

    @property
    def title(self):
        return self.version.title
    
    @property
    def text(self):
        return self.version.text
    
    @property
    def text_hash(self):
        return self.version.text_hash

    @property
    def language(self):
        return self.version.language

    @property
    def date_added(self):
        return self.version.date_added

    @property
    def date_last_seen(self):
        return self.version.date_last_seen

    @property
    def date_published(self):
        return self.version.date_published

    

    # title = models.CharField(max_length=200, blank=True, null=True)
    # text = models.TextField(max_length=None, blank=True, null=True)
    # text_hash = models.CharField(max_length=100, blank=True, unique=True, null=True)
    # language = models.CharField(max_length=200, choices=LANGUAGES, blank=True, null=True)
    # date_added = models.DateTimeField('Date Added', blank=True, null=True)
    # date_last_seen = models.DateTimeField('Date Last Seen', blank=True, null=True)
    # date_published = models.DateTimeField('Date Published', blank=True, null=True)
    # is_referring = models.NullBooleanField(default=None)

    def __str__(self):
        return self.url


class SourceTwitter(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=200)
    matched = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    version = models.ForeignKey(Version)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
