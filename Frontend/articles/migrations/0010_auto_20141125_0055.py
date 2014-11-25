# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20141124_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url_origin',
            field=models.URLField(max_length=2000, verbose_name=b'Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='url_origin',
            field=models.URLField(max_length=2000, verbose_name=b'Site'),
            preserve_default=True,
        ),
    ]
