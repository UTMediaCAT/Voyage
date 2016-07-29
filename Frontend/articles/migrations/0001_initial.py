# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.URLField(max_length=2000, verbose_name=b'Referring Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
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
                ('anchor_text', models.CharField(max_length=2000, verbose_name=b'Anchor Text')),
                ('matched', models.BooleanField(default=False)),
                ('local', models.BooleanField(default=True)),
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
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.URLField(unique=True, max_length=2000, verbose_name=b'URL')),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('text', models.TextField(blank=True)),
                ('text_hash', models.CharField(unique=True, max_length=100, blank=True)),
                ('language', models.CharField(max_length=200, blank=True)),
                ('date_added', models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True)),
                ('date_last_seen', models.DateTimeField(null=True, verbose_name=b'Date Last Seen', blank=True)),
                ('date_published', models.DateTimeField(null=True, verbose_name=b'Date Published', blank=True)),
                ('found_by', models.CharField(max_length=100, blank=True)),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sourcetwitter',
            name='version',
            field=models.ForeignKey(to='articles.Version'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourcesite',
            name='version',
            field=models.ForeignKey(to='articles.Version'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='keyword',
            name='version',
            field=models.ForeignKey(to='articles.Version'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='version',
            field=models.ForeignKey(to='articles.Version'),
            preserve_default=True,
        ),
    ]
