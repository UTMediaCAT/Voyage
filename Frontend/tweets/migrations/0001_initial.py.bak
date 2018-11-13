# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('retweet_count', models.PositiveIntegerField(default=0)),
                ('favorite_count', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=2000)),
                ('domain', models.URLField(max_length=2000, verbose_name=b'Source Site')),
                ('matched', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('matched', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(max_length=200)),
                ('text', models.CharField(default=b'', max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True)),
                ('date_published', models.DateTimeField(null=True, verbose_name=b'Date Published', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sourcetwitter',
            name='tweet',
            field=models.ForeignKey(to='tweets.Tweet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourcesite',
            name='tweet',
            field=models.ForeignKey(to='tweets.Tweet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='keyword',
            name='tweet',
            field=models.ForeignKey(to='tweets.Tweet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='countlog',
            name='tweet',
            field=models.ForeignKey(to='tweets.Tweet'),
            preserve_default=True,
        ),
    ]
