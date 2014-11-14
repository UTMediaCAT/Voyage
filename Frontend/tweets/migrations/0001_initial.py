# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=200)),
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
                ('user', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True)),
                ('date_published', models.DateTimeField(null=True, verbose_name=b'Date Published', blank=True)),
                ('followers', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
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
    ]
