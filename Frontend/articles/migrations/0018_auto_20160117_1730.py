# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_sourcesite_anchor_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='found_by',
            field=models.CharField(default='MediaCAT Crawler', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='language',
            field=models.CharField(default='English', max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
