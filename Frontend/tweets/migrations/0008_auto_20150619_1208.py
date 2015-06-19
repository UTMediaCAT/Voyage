# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0007_auto_20150604_0316'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('retweet_count', models.PositiveIntegerField(default=0)),
                ('favorite_count', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True)),
                ('tweet', models.ForeignKey(to='tweets.Tweet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
	migrations.RenameModel('Source', 'SourceSite'),
	migrations.AddField('SourceSite', 'matched', models.BooleanField()),
        migrations.CreateModel(
            name='SourceTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('matched', models.BooleanField()),
                ('tweet', models.ForeignKey(to='tweets.Tweet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
