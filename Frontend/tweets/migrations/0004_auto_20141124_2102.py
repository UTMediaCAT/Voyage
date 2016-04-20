# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_auto_20141123_1532'),
    ]

    operations = [
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
