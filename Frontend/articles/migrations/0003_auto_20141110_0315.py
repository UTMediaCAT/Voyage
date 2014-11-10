# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20141110_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateField(verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateField(verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='author',
            name='author',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='source',
            name='source',
            field=models.CharField(max_length=200),
        ),
    ]
