# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20160306_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('text', models.TextField(blank=True)),
                ('text_hash', models.CharField(max_length=100, blank=True)),
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
            model_name='author',
            name='version',
            field=models.ForeignKey(default=0, to='articles.Version'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keyword',
            name='version',
            field=models.ForeignKey(default=0, to='articles.Version'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcesite',
            name='version',
            field=models.ForeignKey(default=0, to='articles.Version'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sourcetwitter',
            name='version',
            field=models.ForeignKey(default=0, to='articles.Version'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='url',
            name='name',
            field=models.URLField(max_length=2000, verbose_name=b'URL'),
            preserve_default=True,
        ),
    ]
