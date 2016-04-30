# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0025_auto_20160320_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='name',
            field=models.URLField(unique=True, max_length=2000, verbose_name=b'URL'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='text_hash',
            field=models.CharField(unique=True, max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
