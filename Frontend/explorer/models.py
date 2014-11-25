from django.db import models

# Create your models here.

class Msite(models.Model):
    url = models.URLField(max_length=2000, unique=True, 
                          help_text='Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)')
    name = models.CharField(max_length=200, 
                            help_text='Your favorable alias of this site.\n' +
                                      'Maximum 200 characters')

    class Meta:
        verbose_name = 'Monitoring Site'


    def __unicode__(self):
        return self.name

class Fsite(models.Model):
    url = models.URLField(max_length=2000, unique=True, 
                          help_text='Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://aljazeera.com)')
    name = models.CharField(max_length=200, 
                            help_text='Your favorable alias of this site.')

    class Meta:
        verbose_name = 'Foreign Site'

    def __unicode__(self):
        return self.name

class Keyword(models.Model):
    keyword = models.CharField(max_length=200, unique=True, 
                            help_text='Case insensitive. Maximum 200 characters (Ex. Canada)')

    def __unicode__(self):
        return self.keyword

class Taccount(models.Model):
    account = models.CharField(max_length=200, unique=True, 
                            help_text='Do not include "@". Maximum 200 characters (Ex. CNN)')

    class Meta:
        verbose_name = 'Twitter Account'

    def __unicode__(self):
        return self.account