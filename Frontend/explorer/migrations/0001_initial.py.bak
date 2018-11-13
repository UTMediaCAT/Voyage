# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import explorer.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Case insensitive. Maximum 200 characters (Ex. Canada)', unique=True, max_length=200)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferringSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)', unique=True, max_length=2000)),
                ('name', models.CharField(help_text=b'Your favorable name of this site.\nMaximum 200 characters', unique=True, max_length=200)),
                ('mode', models.PositiveSmallIntegerField(default=0, help_text=b'RSS - Fast but may not work on some sites.<br>MediaCAT Crawler - Slow but compatible with any sites.<br>Both - Uses both Newspaper and MediaCAT CrawlerB for maximum results.', verbose_name=b'Scanner', choices=[(0, b'RSS'), (1, b'MediaCAT Crawler'), (2, b'Both')])),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Referring Site',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferringSiteCssSelector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.PositiveSmallIntegerField(default=0, verbose_name=b'Field', choices=[(0, b'Title'), (1, b'Author'), (2, b'Date Published'), (3, b'Date Modified')])),
                ('pattern', models.CharField(help_text=b'CSS Selector pattern', max_length=1000)),
                ('regex', models.CharField(help_text=b'Regular expression to further narrow down', max_length=1000, blank=True)),
                ('site', models.ForeignKey(to='explorer.ReferringSite')),
            ],
            options={
                'verbose_name': 'CSS Selector',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferringSiteFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(help_text=b'Any URL that matches the pattern will be ignored from the crawler.', max_length=1000)),
                ('regex', models.BooleanField(default=False, help_text=b'Use Regular Expression instead of string comparison.')),
                ('site', models.ForeignKey(to='explorer.ReferringSite')),
            ],
            options={
                'verbose_name': 'Filter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferringTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user])),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Referring Twitter Account',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://aljazeera.com)', unique=True, max_length=2000)),
                ('name', models.CharField(help_text=b'Your favorable name of this site.', unique=True, max_length=200)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Source Site',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceSiteAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text=b'Case insensitive. Maximum 200 characters (Ex. Canada)', unique=True, max_length=200)),
                ('primary', models.ForeignKey(to='explorer.SourceSite')),
            ],
            options={
                'verbose_name': 'Alias',
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user])),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Source Twitter Account',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceTwitterAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user])),
                ('primary', models.ForeignKey(to='explorer.SourceTwitter')),
            ],
            options={
                'verbose_name': 'Alias',
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
    ]
