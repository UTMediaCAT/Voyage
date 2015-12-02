# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20150619_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_modified',
            field=models.DateTimeField(null=True, verbose_name=b'Date Modified', blank=True),
            preserve_default=True,
        ),
    ]
