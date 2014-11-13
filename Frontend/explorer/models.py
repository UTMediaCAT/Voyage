from django.db import models

# Create your models here.

class Msite(models.Model):
    url = models.URLField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    influence = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Monitoring Site'


    def __unicode__(self):
        return self.name

class Fsite(models.Model):
    url = models.URLField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    influence = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Foreign Site'

    def __unicode__(self):
        return self.name

class Keyword(models.Model):
    keyword = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.keyword

class Taccount(models.Model):
    account = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.account