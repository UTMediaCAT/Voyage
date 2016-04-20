# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20141110_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateField(verbose_name=b'Date Added', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateField(verbose_name=b'Date Published', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='influence',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
