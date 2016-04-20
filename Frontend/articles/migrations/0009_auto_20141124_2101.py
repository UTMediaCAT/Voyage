# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20141123_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='url_origin',
            field=models.URLField(verbose_name=b'Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='url',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='url_origin',
            field=models.URLField(verbose_name=b'Site'),
            preserve_default=True,
        ),
    ]
